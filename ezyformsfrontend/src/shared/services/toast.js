// src/shared/toast.js
import { useToast } from "vue-toastification";

const toast = useToast();

// Basic types
export function showSuccess(message, options = {}) {
    toast.success(message, {
    ...options,
    toastClassName: "custom-toast-padding"
  });
}

export function showError(message, options = {}) {
  toast.error(message, {
    ...options,
    toastClassName: "custom-toast-padding"
  });
}

export function showInfo(message, options = {}) {
  toast.info(message, {
    ...options,
    toastClassName: "custom-toast-padding"
  });
}

export function showWarning(message, options = {}) {
  toast.warning(message, {
    ...options,
    toastClassName: "custom-toast-padding"
  });
}

// Neutral/default toast
export function showDefault(message, options = {}) {
  toast(message, {
    ...options,
    toastClassName: "custom-toast-padding"
  }); // no type, just neutral
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
