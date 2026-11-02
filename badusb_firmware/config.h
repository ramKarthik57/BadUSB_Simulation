#pragma once

#include <Arduino.h>

// ============================================================
// HARDWARE DEFINITIONS
// ============================================================
#define PIN_BOOT_BUTTON     0       // On-board BOOT button on ESP32-S3 DevKit
#define BUTTON_DEBOUNCE_MS  50      // Debounce polling interval in milliseconds
#define BUTTON_HOLD_COOLDOWN_MS 600 // Minimum time between consecutive button triggers

// ============================================================
// USB HID CONFIGURATION
// ============================================================
#define USB_MANUFACTURER    "TinyUSB"
#define USB_PRODUCT         "BadUSB Demo"
#define USB_SERIAL          "123456"
#define USB_POWER_MA        100
#define USB_ENUM_TIMEOUT_MS 3500    // Bounded wait time for USB ready on boot

// ============================================================
// WI-FI CONFIGURATION
// ============================================================
// Dual Mode: SoftAP + Station (to connect to phone's hotspot)
#define DEFAULT_AP_SSID     "BadUSB-Controller"
#define DEFAULT_AP_PASS     "badusb_control"  // Minimum 8 characters for WPA2
#define DEFAULT_AP_CHANNEL  1

// Preconfigured Phone Hotspot credentials (User can also update via Settings)
#define DEFAULT_STA_SSID    "AndroidAP_4786"  // Phone hotspot SSID
#define DEFAULT_STA_PASS    "12345678"        // Phone hotspot Password

#define MDNS_HOSTNAME       "badusb"          // Accessible at http://badusb.local
#define HTTP_PORT           80

// ============================================================
// SECURITY & AUTHENTICATION
// ============================================================
#define DEFAULT_AUTH_PIN    "badusb123"       // Required PIN to execute commands
#define AUTH_TOKEN_MAX_LEN  32
#define MAX_TEXT_PAYLOAD_LEN 256              // Bounded text message length
#define MAX_COMMAND_RATE_MS 100               // Rate limit between rapid web commands

// ============================================================
// SCENARIO DEFINITIONS
// ============================================================
#define TOTAL_SCENARIOS     4
#define SCENARIO_1_NAME     "Notepad Awareness"
#define SCENARIO_2_NAME     "Portal Redirection"
#define SCENARIO_3_NAME     "Ransomware Awareness"
#define SCENARIO_4_NAME     "Wi-Fi Reconnaissance"

// Inter-key typing delays (milliseconds)
#define KEY_PRESS_DELAY_MS  30
#define KEY_RELEASE_DELAY_MS 30
#define STEP_PAUSE_SHORT_MS 200
#define STEP_PAUSE_MEDIUM_MS 1000
#define STEP_PAUSE_LONG_MS  1500
