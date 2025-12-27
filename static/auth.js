function register() {
  const username = document.getElementById("register-username").value;
  const password = document.getElementById("register-password").value;

  fetch("/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.location.href = "/";
      } else {
        alert(data.error);
      }
    });
}

function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.location.href = "/dashboard";
      } else {
        alert(data.error);
      }
    });
}

function deleteAccount() {
  if (!confirm("Are you sure you want to delete your account? This cannot be undone.")) {
    return;
  }

  fetch("/api/delete_account", {
    method: "POST"
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("Account deleted.");
        window.location.href = "/";
      } else {
        alert(data.error || "Failed to delete account.");
      }
    });
}
