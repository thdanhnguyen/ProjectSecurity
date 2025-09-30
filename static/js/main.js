// Main JavaScript File
// Các hàm tiện ích và xử lý UI

// Toggle password visibility
function togglePassword(inputId) {
  const input = document.getElementById(inputId)
  const button = input.nextElementSibling

  if (input.type === "password") {
    input.type = "text"
    button.textContent = "🙈"
  } else {
    input.type = "password"
    button.textContent = "👁️"
  }
}

// Show flash message dynamically
function showFlash(category, message) {
  const container = document.querySelector(".flash-container") || createFlashContainer()

  const flash = document.createElement("div")
  flash.className = `flash-message flash-${category}`

  const icons = {
    success: "✓",
    error: "✕",
    warning: "⚠",
    info: "ℹ",
  }

  flash.innerHTML = `
        <span class="flash-icon">${icons[category] || "ℹ"}</span>
        <span class="flash-text">${message}</span>
        <button class="flash-close" onclick="this.parentElement.remove()">×</button>
    `

  container.appendChild(flash)

  // Auto remove after 5 seconds
  setTimeout(() => {
    flash.remove()
  }, 5000)
}

function createFlashContainer() {
  const container = document.createElement("div")
  container.className = "flash-container"
  document.body.appendChild(container)
  return container
}

// Auto-hide flash messages
document.addEventListener("DOMContentLoaded", () => {
  const flashMessages = document.querySelectorAll(".flash-message")

  flashMessages.forEach((flash) => {
    setTimeout(() => {
      flash.style.animation = "slideOut 0.3s ease"
      setTimeout(() => flash.remove(), 300)
    }, 5000)
  })
})

// Form validation
function validateForm(formId) {
  const form = document.getElementById(formId)
  if (!form) return true

  const inputs = form.querySelectorAll("input[required]")
  let isValid = true

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.style.borderColor = "var(--danger)"
      isValid = false
    } else {
      input.style.borderColor = "var(--border)"
    }
  })

  return isValid
}

// Email validation
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Password strength checker
function checkPasswordStrength(password) {
  let strength = 0

  if (password.length >= 8) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^a-zA-Z0-9]/.test(password)) strength++

  return strength
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  })
})

// Loading state for buttons
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true
    button.dataset.originalText = button.textContent
    button.textContent = "Đang xử lý..."
  } else {
    button.disabled = false
    button.textContent = button.dataset.originalText
  }
}

// Copy to clipboard
function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      showFlash("success", "Đã sao chép vào clipboard")
    })
    .catch(() => {
      showFlash("error", "Không thể sao chép")
    })
}

// Confirm dialog
function confirmAction(message) {
  return confirm(message)
}

// Format date
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

// Debounce function
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Console log for debugging
console.log("🔐 Secure Auth System - JavaScript Loaded")
