// src/shared/toast.js
import { useToast } from "vue-toastification";

const toast = useToast();

// Basic types
export function showSuccess(message, options = {}) {
  toast.success(message, options);
}

export function showError(message, options = {}) {
  toast.error(message, options);
}

export function showInfo(message, options = {}) {
  toast.info(message, options);
}

export function showWarning(message, options = {}) {
  toast.warning(message, options);
}

// Neutral/default toast
export function showDefault(message, options = {}) {
  toast(message, options); // no type, just neutral
}

// Custom toast with icon, style, or HTML content
export function showCustom(message, options = {}) {
  toast(message, {
    ...options,
    icon: options.icon || "⭐",   // default custom icon
    timeout: options.timeout || 5000,
    hideProgressBar: options.hideProgressBar ?? false,
    ...options
  });
}
