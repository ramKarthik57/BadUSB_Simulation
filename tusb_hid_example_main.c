/*
 Final Stable BadUSB Multi-Payload Demo ESP32-S3
*/

#include <stdlib.h>
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "tinyusb.h"
#include "class/hid/hid_device.h"
#include "driver/gpio.h"

#define APP_BUTTON GPIO_NUM_0

static const char *TAG = "badusb";

#define TUSB_DESC_TOTAL_LEN (TUD_CONFIG_DESC_LEN + CFG_TUD_HID * TUD_HID_DESC_LEN)

static int payload_id = 1;
static bool finished = false;



/******** DESCRIPTORS ********/

const uint8_t hid_report_descriptor[] = {
    TUD_HID_REPORT_DESC_KEYBOARD(HID_REPORT_ID(HID_ITF_PROTOCOL_KEYBOARD))
};

const char* hid_string_descriptor[5] = {
    (char[]){0x09,0x04},
    "TinyUSB",
    "BadUSB Demo",
    "123456",
    "HID",
};

static const uint8_t hid_configuration_descriptor[] = {

    TUD_CONFIG_DESCRIPTOR(
        1,1,0,
        TUSB_DESC_TOTAL_LEN,
        TUSB_DESC_CONFIG_ATT_REMOTE_WAKEUP,
        100),

    TUD_HID_DESCRIPTOR(
        0,4,false,
        sizeof(hid_report_descriptor),
        0x81,16,10),
};



/******** HID ********/

uint8_t const *tud_hid_descriptor_report_cb(uint8_t instance)
{
    return hid_report_descriptor;
}

uint16_t tud_hid_get_report_cb(
    uint8_t instance,
    uint8_t report_id,
    hid_report_type_t report_type,
    uint8_t* buffer,
    uint16_t reqlen)
{
    return 0;
}

void tud_hid_set_report_cb(
    uint8_t instance,
    uint8_t report_id,
    hid_report_type_t report_type,
    uint8_t const* buffer,
    uint16_t bufsize)
{
}



/******** KEYBOARD ********/

static void send_char(char c)
{
    uint8_t keycode[6] = {0};
    uint8_t mod = 0;

    if (c >= 'a' && c <= 'z')
        keycode[0] = HID_KEY_A + (c - 'a');

    else if (c >= 'A' && c <= 'Z') {
        keycode[0] = HID_KEY_A + (c - 'A');
        mod = KEYBOARD_MODIFIER_LEFTSHIFT;
    }

    else if (c >= '1' && c <= '9')
        keycode[0] = HID_KEY_1 + (c - '1');

    else if (c == '0')
        keycode[0] = HID_KEY_0;

    else if (c == ' ')
        keycode[0] = HID_KEY_SPACE;

    else if (c == '\n')
        keycode[0] = HID_KEY_ENTER;

    else if (c == '.')
        keycode[0] = HID_KEY_PERIOD;

    else if (c == '/')
        keycode[0] = HID_KEY_SLASH;

    else if (c == '\\')
        keycode[0] = HID_KEY_BACKSLASH;

    else if (c == '-')
        keycode[0] = HID_KEY_MINUS;

    else if (c == '_') {
        keycode[0] = HID_KEY_MINUS;
        mod = KEYBOARD_MODIFIER_LEFTSHIFT;
    }

    else if (c == ':') {
        keycode[0] = HID_KEY_SEMICOLON;
        mod = KEYBOARD_MODIFIER_LEFTSHIFT;
    }

    else if (c == '%') {
        keycode[0] = HID_KEY_5;
        mod = KEYBOARD_MODIFIER_LEFTSHIFT;
    }

    tud_hid_keyboard_report(
        HID_ITF_PROTOCOL_KEYBOARD,
        mod,
        keycode);

    vTaskDelay(pdMS_TO_TICKS(40));

    tud_hid_keyboard_report(
        HID_ITF_PROTOCOL_KEYBOARD,
        0,
        NULL);

    vTaskDelay(pdMS_TO_TICKS(40));
}


static void send_string(const char *s)
{
    while (*s)
    {
        send_char(*s);
        s++;
    }
}



/******** OPEN RUN ********/

static void open_run()
{
    uint8_t keycode[6] = {HID_KEY_R};

    tud_hid_keyboard_report(
        HID_ITF_PROTOCOL_KEYBOARD,
        KEYBOARD_MODIFIER_LEFTGUI,
        keycode);

    vTaskDelay(pdMS_TO_TICKS(150));

    tud_hid_keyboard_report(
        HID_ITF_PROTOCOL_KEYBOARD,
        0,
        NULL);

    vTaskDelay(pdMS_TO_TICKS(1000));
}



/******** PAYLOADS ********/

static void payload_notepad()
{
    open_run();

    send_string("notepad\n");

    vTaskDelay(pdMS_TO_TICKS(1500));

    send_string("BadUSB Simulation using ESP32 S3 Devkit\n");

    vTaskDelay(pdMS_TO_TICKS(200));

    send_string("This computer accepted keystrokes from an unknown USB device.\n");

    vTaskDelay(pdMS_TO_TICKS(200));

    send_string("Always be careful when plugging unknown USB drives.\n");
}


static void payload_website()
{
    open_run();

    send_string("cmd\n");

    vTaskDelay(pdMS_TO_TICKS(1000));

    send_string("start https://my.amrita.edu\n");
}


static void payload_awareness()
{
    open_run();

    send_string("powershell -ExecutionPolicy Bypass\n");

    vTaskDelay(pdMS_TO_TICKS(1500));

    send_string("& \"C:\\Users\\Ram\\Documents\\ransomware_awareness_demo.ps1\"\n");
}


static void payload_wifi_demo()
{
    // Open Run dialog (Win + R)
    open_run();
    vTaskDelay(pdMS_TO_TICKS(500));

    // Start Command Prompt
    send_string("cmd\n");
    vTaskDelay(pdMS_TO_TICKS(1000));

    // Run the command
    send_string("netsh wlan show profiles\n");
}



/******** SELECTOR ********/

static void run_payload(int id)
{
    if (id == 1) payload_notepad();
    else if (id == 2) payload_website();
    else if (id == 3) payload_awareness();
    else if (id == 4) payload_wifi_demo();
}



/******** MAIN ********/

void app_main(void)
{
    gpio_config_t io = {
        .pin_bit_mask = BIT64(APP_BUTTON),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = true,
    };

    gpio_config(&io);


    const tinyusb_config_t tusb_cfg = {

        .device_descriptor = NULL,

        .string_descriptor = hid_string_descriptor,

        .string_descriptor_count =
            sizeof(hid_string_descriptor) /
            sizeof(hid_string_descriptor[0]),

        .external_phy = false,

        .configuration_descriptor =
            hid_configuration_descriptor,
    };

    tinyusb_driver_install(&tusb_cfg);


    while (1)
    {
        if (tud_mounted() && !finished)
        {
            run_payload(payload_id);

            while (gpio_get_level(APP_BUTTON))
            {
                vTaskDelay(pdMS_TO_TICKS(50));
            }

            payload_id++;

            if (payload_id > 4)
                finished = true;

            vTaskDelay(pdMS_TO_TICKS(1000));
        }

        vTaskDelay(pdMS_TO_TICKS(100));
    }
}