# Functional Specification Document (FSD)
## Authentication & Account Management API

**Project:** User Authentication System  
**Version:** 1.0  
**Date:** 2026-03-18  
**Base URL:** `http://localhost:8020/api/v1/accounts/`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Configuration](#2-configuration)
3. [Registration](#3-registration)
4. [Login Flow](#4-login-flow)
   - 4.1 [OTP-Enabled Mode](#41-otp-enabled-mode-auth_otp_enabled--true)
   - 4.2 [OTP-Disabled Mode](#42-otp-disabled-mode-auth_otp_enabled--false)
5. [OTP Verification](#5-otp-verification)
6. [Resend OTP](#6-resend-otp)
7. [Forgot Password Flow](#7-forgot-password-flow)
   - 7.1 [Step 1 – Request OTP](#71-step-1--request-password-reset-otp)
   - 7.2 [Step 2 – Verify Reset OTP](#72-step-2--verify-reset-otp)
   - 7.3 [Step 3 – Reset Password](#73-step-3--reset-password)
8. [Token Refresh](#8-token-refresh)
9. [Password Change](#9-password-change)
10. [Email Change](#10-email-change)
    - 10.1 [Step 1 – Request Email Change OTP](#101-step-1--request-email-change-otp)
    - 10.2 [Step 2 – Verify Email Change OTP](#102-step-2--verify-email-change-otp)
11. [Error Handling](#11-error-handling)
12. [Security & Business Rules](#12-security--business-rules)
13. [Data Models](#13-data-models)
14. [API Summary Table](#14-api-summary-table)

---

## 1. Overview

This document describes the complete functional specification of a Token-based (JWT) Authentication system. The system supports user registration, OTP-based email verification, login, password reset, password change, and email change.

---

### Feature List

#### 🔐 Authentication
| # | Feature | Description |
|---|---|---|
| 1 | **JWT Authentication** | Stateless authentication using `access` token (15 min) and `refresh` token (7 days). Access token can be silently renewed via `/refresh/` without re-login. |
| 2 | **Configurable OTP Mode** | `AUTH_OTP_ENABLED = True` → OTP required on every login. `False` → OTP required only on first login for email verification. |
| 3 | **First Login Email Verification** | On first login, an OTP is sent to the user's email. JWT tokens are issued only after successful OTP verification, ensuring the email address is valid and owned by the user. |
| 4 | **Auto Login After Registration** | When `AUTO_LOGIN_AFTER_REGISTRATION = True`, a JWT access token is returned immediately upon successful registration — skipping the manual login step entirely. |

#### 📧 OTP System
| # | Feature | Description |
|---|---|---|
| 4 | **OTP via Email** | 6-digit numeric OTP sent to user's registered email address. |
| 5 | **OTP Expiry** | Login/verification OTP expires after `OTP_EXPIRY_TIME` (300 seconds). |
| 6 | **OTP Resend** | User can request a new OTP. Controlled by `OTP_RESEND_COOLDOWN` (60 seconds between requests). |
| 7 | **IP-Based Resend Throttling** | `/resend-otp/` enforces a custom IP-based throttle — max **1 request per IP every 5 minutes**, regardless of the email used. Prevents OTP spam/abuse. |

#### 🛡️ Security & Abuse Prevention
| # | Feature | Description |
|---|---|---|
| 8 | **Failed Login Attempt Tracking** | Every wrong password increments `failed_login_attempts` counter on the user record. |
| 9 | **Auto Account Lock** | After too many failed login attempts, `account_locked_until` is set — user cannot log in until the lock period expires. |
| 10 | **Auto Email Un-verification on Excessive Failures** | After repeated failed login attempts beyond a threshold, `is_email_verified` is reset to `False`, forcing the user to re-verify their email on next login. |
| 10a | **Auto Email Un-verification on Forgot Password** | Calling `/forgot-password/` resets `is_email_verified = False`. `email_verified_at` is **kept as-is** — a non-null value means the account was previously verified, helping distinguish from accounts that were never verified. Email is re-verified when `/verify-reset-otp/` succeeds. |
| 11 | **Failed Attempt Reset on Success** | On successful login, `failed_login_attempts` is reset to `0` automatically. |
| 12 | **Email Enumeration Protection** | `/forgot-password/` always returns `202 Accepted` regardless of whether the email exists in the system, preventing attackers from discovering registered emails. |

#### 🔁 Password Reset
| # | Feature | Description |
|---|---|---|
| 13 | **OTP-Based Password Reset** | 3-step process: request OTP → verify OTP → reset password. Each step is time-limited. |
| 14 | **Time-Limited Reset OTP** | Reset OTP expires after `RESET_OTP_EXPIRY` (300 seconds). |
| 15 | **Time-Limited Reset Token** | `reset_token` issued after OTP verification expires after `RESET_TOKEN_EXPIRY` (600 seconds). |
| 16 | **Single-Use Reset Token** | `reset_token` is invalidated immediately after use — cannot be reused. |
| 17 | **Last Password Change Record** | `last_password_change` datetime is recorded every time the user successfully resets their password. |

#### 🔑 Account Management (Authenticated)
| # | Feature | Description |
|---|---|---|
| 18 | **Password Change** | Authenticated user can change password by providing current + new password. Requires valid `access` token. |
| 19 | **Global Logout on Password Change** | Changing password updates `token_invalidated_at` — all previously issued access/refresh tokens become invalid immediately, forcing logout from all devices. |
| 20 | **Email Change (OTP-Verified)** | Authenticated user can request an email change. OTP is sent to the new email address for verification before the change is applied. |
| 21 | **Global Logout on Email Change** | Changing email updates `token_invalidated_at` and `password_changed_at` — all previously issued tokens are invalidated across all devices. |
| 22 | **Email Change OTP Throttling** | `/email/change/` enforces a throttle — max **1 request per 3 minutes** to prevent OTP spam. |
| 23 | **Email Change OTP Expiry** | Email change OTP expires after `OTP_EXPIRY_TIME` (300 seconds). |

#### 📋 Audit & Record Keeping
| # | Feature | Description |
|---|---|---|
| 24 | **Last Login Record** | `last_login` datetime is updated on every successful authentication. |
| 25 | **Password Change History** | `password_changed_at` records when the password was last changed (both via forgot-password and password change). |
| 26 | **Email Change History** | `email_changed_at` records when the email was last successfully changed. |
| 27 | **Failed Login History** | `failed_login_attempts` counter provides visibility into brute-force attempts on an account. |
| 28 | **Token Invalidation Record** | `token_invalidated_at` records the last time all tokens were invalidated (password or email change). |

---

## 2. Configuration

### Registration Process

| Configuration Key               | Type    | Default | Description |
|---------------------------------|---------|---------|-------------|
| `AUTO_LOGIN_AFTER_REGISTRATION` | Boolean | `True`  | `True` → JWT access token is returned immediately in the registration response. `False` → User must log in manually after registration. |

### OTP Base Login

| Configuration Key      | Type    | Default | Description |
|------------------------|---------|---------|-------------|
| `AUTH_OTP_ENABLED`     | Boolean | `False` | `True` → OTP required on **every** login. `False` → OTP required only on **first login** (initial email verification after registration). |
| `OTP_EXPIRY_TIME`      | Integer | `300`   | Login/verification OTP expiry time in **seconds**. After this time the OTP becomes invalid. |
| `OTP_RESEND_COOLDOWN`  | Integer | `60`    | Minimum wait time in **seconds** before a user can request a new OTP. Applies to both login OTP and reset OTP resend. |

### JWT Token

| Configuration Key        | Type    | Default  | Description |
|--------------------------|---------|----------|-------------|
| `ACCESS_TOKEN_LIFETIME`  | Integer | `15 min` | Access token validity duration. Expires **15 minutes** after issuance. |
| `REFRESH_TOKEN_LIFETIME` | Integer | `7 days` | Refresh token validity duration. Expires **7 days** after issuance. |

### Forget Password Process

| Configuration Key      | Type    | Default | Description |
|------------------------|---------|---------|-------------|
| `RESET_OTP_EXPIRY`     | Integer | `300`   | Seconds until the password-reset OTP (sent via email) expires. User must call `/verify-reset-otp/` within this window. |
| `RESET_TOKEN_EXPIRY`   | Integer | `600`   | Seconds until the `reset_token` (issued after OTP verification) expires. User must call `/reset-password/` within this window. |
| `OTP_RESEND_COOLDOWN`  | Integer | `60`    | Shared with login section — minimum wait in seconds before resending a reset OTP. |

---

## 3. Registration

### Endpoint
```
POST /api/v1/accounts/register/
```

### Request Body
```json
{
  "first_name": "AN",
  "last_name": "Mamun",
  "email": "anmamuncoder@gmail.com",
  "password": "securepassword123"
}
```

### Success Response — `201 Created`

#### When `AUTO_LOGIN_AFTER_REGISTRATION = True`
User is automatically authenticated — JWT access token is returned directly.
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "access": "<JWT_ACCESS_TOKEN>"
  }
}
```

#### When `AUTO_LOGIN_AFTER_REGISTRATION = False`
No token is issued — user must log in manually.
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "email": "anmamuncoder@gmail.com",
    "first_name": "AN",
    "last_name": "Mamun"
  }
}
```

### Business Rules
- Email must be unique in the system.
- Password is stored hashed (never plain text).
- After registration, `is_email_verified = False`.
- If `AUTO_LOGIN_AFTER_REGISTRATION = True`, a JWT access token is issued immediately — no separate login step required.
- If `AUTO_LOGIN_AFTER_REGISTRATION = False`, no token is issued — OTP is triggered at first login.

---

## 4. Login Flow

### Endpoint
```
POST /api/v1/accounts/login/
```

### Request Body
```json
{
  "email": "anmamuncoder@gmail.com",
  "password": "securepassword123"
}
```

---

### 4.1 OTP-Enabled Mode (`AUTH_OTP_ENABLED = True`)

**Every login** requires OTP verification regardless of email verification status.

**Flow:**
```
Login Request → Credentials Valid → Send OTP → OTP Verification → JWT Tokens Issued
```

**Response from `/login/`:**
```json
{
  "success": true,
  "message": "OTP sent to your email",
  "data": null
}
```
→ User must then call `/verify-otp/` to complete login.

---

### 4.2 OTP-Disabled Mode (`AUTH_OTP_ENABLED = False`)

#### Case A — First Login (Email Not Yet Verified)

**Flow:**
```
Login Request → Credentials Valid → Email Not Verified → Send OTP → OTP Verification → JWT Tokens Issued
```

**Response from `/login/`:**
```json
{
  "success": true,
  "message": "OTP sent to your email",
  "data": null
}
```
→ User must then call `/verify-otp/` to complete login.

#### Case B — Subsequent Logins (Email Already Verified)

**Flow:**
```
Login Request → Credentials Valid → Email Verified → JWT Tokens Issued Directly
```

**Response from `/login/`:**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "access": "<JWT_ACCESS_TOKEN>",
    "refresh": "<JWT_REFRESH_TOKEN>"
  }
}
```
→ Tokens returned immediately. No OTP step required.

**Side Effects on Successful Login:**
- `user.last_login` is updated with the current datetime.
- `user.failed_login_attempts` is reset to `0`.

---

### Login Failure Response
```json
{
  "status": false,
  "errors": {
    "non_field_errors": ["Invalid credentials"]
  }
}
```

**Business Rule:** If the email exists in the system but the password is incorrect, `user.failed_login_attempts` is incremented by `1`.

---

## 5. OTP Verification

### Endpoint
```
POST /api/v1/accounts/verify-otp/
```

### Request Body
```json
{
  "email": "anmamuncoder@gmail.com",
  "otp": "486724"
}
```

### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "access": "<JWT_ACCESS_TOKEN>",
    "refresh": "<JWT_REFRESH_TOKEN>"
  }
}
```

### Business Rules
- OTP is a 6-digit numeric code sent to the user's email.
- OTP has a limited validity window (server-configured).
- On successful verification:
  - `user.is_email_verified` is set to `True`.
  - `user.email_verified_at` is updated to the current datetime.
  - `user.last_login` is updated.
  - JWT access and refresh tokens are issued.

---

## 6. Resend OTP

### Endpoint
```
POST /api/v1/accounts/resend-otp/
```

### Request Body
```json
{
  "email": "anmamuncoder@gmail.com"
}
```

### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "OTP resent successfully",
  "data": null
}
```

### Rate-Limited Response — `429 Too Many Requests`
```json
{
  "status": false,
  "errors": {
    "detail": "Request was throttled. Expected available in 270 seconds."
  }
}
```

### Throttle Rules
- Rate limiting is enforced via a **custom IP-based throttle**.
- Only **1 request per IP address every 5 minutes** is allowed.
- Limit applies regardless of which email address is used in the request body.
- This endpoint is used only during the email verification stage, not for password reset.

---

## 7. Forgot Password Flow

Password reset involves three sequential API calls. Each step has a time constraint enforced by server configuration.

```
Step 1: Request OTP  →  Step 2: Verify OTP  →  Step 3: Reset Password
```

---

### 7.1 Step 1 – Request Password Reset OTP

#### Endpoint
```
POST /api/v1/accounts/forgot-password/
```

#### Request Body
```json
{
  "email": "anmamuncoder@gmail.com"
}
```

#### Response — `202 Accepted` (always, regardless of whether email exists)
```json
{
  "success": true,
  "message": "If the email exists, a reset OTP has been sent",
  "data": null
}
```

#### Business Rules
- Always returns `202 Accepted` to prevent **email enumeration attacks**.
- If the email exists, an OTP is sent to that address.
- The OTP is valid for `RESET_OTP_EXPIRY` seconds.
- **Auto Email Un-verification:** On receiving this request (if email exists), `user.is_email_verified` is reset to `False`. `user.email_verified_at` is **not changed** — it retains the previous verification timestamp. This allows the system to distinguish between an account that was never verified (`email_verified_at = null`) and one that was verified but is currently undergoing a password reset (`email_verified_at = <previous datetime>`).

---

### 7.2 Step 2 – Verify Reset OTP

#### Endpoint
```
POST /api/v1/accounts/verify-reset-otp/
```

> ⚠️ Must be called within `RESET_OTP_EXPIRY` seconds of Step 1.

#### Request Body
```json
{
  "email": "anmamuncoder@gmail.com",
  "otp": "941378"
}
```

#### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "OTP verified",
  "data": {
    "reset_token": "jfBv8Kom4WvtNaDoyjVfjRUyJAOwG2r43phu5LE9K3U"
  }
}
```

#### Failure Response — `400 Bad Request`
```json
{
  "status": false,
  "errors": ["Invalid OTP"]
}
```

#### Business Rules
- `reset_token` is a secure, single-use token.
- `reset_token` is valid for `RESET_TOKEN_EXPIRY` seconds.
- Invalid or expired OTP returns an error.
- On success, `user.is_email_verified` is set to `True` and `user.email_verified_at` is updated to the current datetime.

---

### 7.3 Step 3 – Reset Password

#### Endpoint
```
POST /api/v1/accounts/reset-password/
```

> ⚠️ Must be called within `RESET_TOKEN_EXPIRY` seconds of Step 2.

#### Request Body
```json
{
  "reset_token": "jfBv8Kom4WvtNaDoyjVfjRUyJAOwG2r43phu5LE9K3U",
  "new_password": "newSecurePassword456"
}
```

#### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "Password reset successful",
  "data": null
}
```

#### Failure Response — `400 Bad Request` (Invalid or Expired Token)
```json
{
  "status": false,
  "errors": ["Invalid reset token"]
}
```

#### Business Rules
- `reset_token` is consumed on use (single-use only).
- Invalid or expired `reset_token` returns `400` with `"Invalid reset token"`.
- On success, `user.last_password_change` is updated with the current datetime.
- After reset, the user must log in again with the new password.

---

## 8. Token Refresh

### Endpoint
```
POST /api/v1/accounts/refresh/
```

### Request Body
```json
{
  "refresh": "<JWT_REFRESH_TOKEN>"
}
```

### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "Access token generated",
  "data": {
    "access": "<NEW_JWT_ACCESS_TOKEN>"
  }
}
```

### Failure Response — `400 Bad Request`
```json
{
  "status": false,
  "errors": ["Invalid refresh token"]
}
```

### Business Rules
- A valid `refresh` token must be provided in the request body.
- On success, a **new `access` token** is returned (valid for 15 minutes).
- The `refresh` token itself is **not rotated** — the same refresh token remains valid until it expires (7 days).
- An invalid, malformed, or expired `refresh` token returns `400` with `"Invalid refresh token"`.
- No re-authentication (email/password) is required as long as the refresh token is valid.

---

## 9. Password Change

> 🔒 **Authentication required** — valid `access` token must be provided in the `Authorization: Bearer <token>` header.

### Endpoint
```
PUT /api/v1/accounts/password/change/
```

### Request Body
```json
{
  "current_password": "1234567890",
  "new_password": "123456789012",
  "confirm_password": "123456789012"
}
```

### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "Password updated successfully.",
  "data": null
}
```

### Failure Response — Wrong Current Password `400 Bad Request`
```json
{
  "status": false,
  "errors": {
    "current_password": ["Current password is incorrect."]
  }
}
```

### Business Rules
- User must be authenticated (valid `access` token required).
- `current_password` must match the user's existing password.
- `new_password` and `confirm_password` must match.
- On success:
  - `user.password` is updated (hashed).
  - `user.password_changed_at` is updated to the current datetime.
  - `user.token_invalidated_at` is updated to the current datetime — **all previously issued access and refresh tokens are immediately invalidated**, logging the user out from all devices.

---

## 10. Email Change

Email change is a two-step authenticated process. An OTP is sent to the **new** email address to verify ownership before the change is applied.

```
Step 1: Request OTP to new email  →  Step 2: Verify OTP → Email Updated
```

---

### 10.1 Step 1 – Request Email Change OTP

> 🔒 **Authentication required.**

#### Endpoint
```
POST /api/v1/accounts/email/change/
```

#### Request Body
```json
{
  "new_email": "newemail@gmail.com",
  "password": "currentpassword"
}
```

#### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "OTP sent to newemail@gmail.com.",
  "data": null
}
```

#### Failure Responses — `400 Bad Request`

Same email as current:
```json
{
  "status": false,
  "errors": {
    "new_email": ["New email must be different from current email."]
  }
}
```

Wrong password:
```json
{
  "status": false,
  "errors": {
    "password": ["Incorrect password."]
  }
}
```

Email already in use by another account:
```json
{
  "status": false,
  "errors": {
    "new_email": ["This email is already in use."]
  }
}
```

#### Throttle & Business Rules
- User must be authenticated (valid `access` token required).
- `password` must match the user's current password.
- `new_email` must be unique across the system and different from the current email.
- OTP is sent to `new_email` (not the current email).
- `user.pending_email` is set to `new_email` until verification is complete.
- `user.email_change_otp` and `user.email_change_otp_created_at` are stored for verification.
- **Throttle:** Max **1 request per 3 minutes** per user. Prevents OTP spam to arbitrary email addresses.
- OTP expires after `OTP_EXPIRY_TIME` (300 seconds).

---

### 10.2 Step 2 – Verify Email Change OTP

> 🔒 **Authentication required.**

#### Endpoint
```
POST /api/v1/accounts/email/change/verify/
```

> ⚠️ Must be called within `OTP_EXPIRY_TIME` seconds of Step 1.

#### Request Body
```json
{
  "otp": "09682"
}
```

#### Success Response — `200 OK`
```json
{
  "success": true,
  "message": "Email updated successfully.",
  "data": null
}
```

#### Failure Response — `400 Bad Request`
```json
{
  "status": false,
  "errors": {
    "otp": ["Invalid OTP."]
  }
}
```

#### Business Rules
- User must be authenticated (valid `access` token required).
- OTP must match `user.email_change_otp` and must not be expired.
- On success:
  - `user.email` is updated to `user.pending_email`.
  - `user.pending_email` is cleared to `null`.
  - `user.email_changed_at` is updated to the current datetime.
  - `user.password_changed_at` is updated to the current datetime.
  - `user.token_invalidated_at` is updated to the current datetime — **all previously issued access and refresh tokens are immediately invalidated**, logging the user out from all devices.
  - `user.email_change_otp` and `user.email_change_otp_created_at` are cleared.

---

## 11. Error Handling

| Scenario | HTTP Status | Response Format |
|---|---|---|
| Invalid credentials | `400` | `{ "status": false, "errors": { "non_field_errors": ["Invalid credentials"] } }` |
| Invalid / expired refresh token | `400` | `{ "status": false, "errors": ["Invalid refresh token"] }` |
| Invalid / expired OTP | `400` | `{ "status": false, "errors": ["Invalid OTP"] }` |
| Rate limit exceeded | `429` | `{ "status": false, "errors": { "detail": "Request was throttled. Expected available in N seconds." } }` |
| Invalid / expired reset token | `400` | `{ "status": false, "errors": ["Invalid reset token"] }` |
| Validation error | `400` | `{ "status": false, "errors": { "<field>": ["<error message>"] } }` |
| Wrong current password | `400` | `{ "status": false, "errors": { "current_password": ["Current password is incorrect."] } }` |
| New email same as current | `400` | `{ "status": false, "errors": { "new_email": ["New email must be different from current email."] } }` |
| Email already in use | `400` | `{ "status": false, "errors": { "new_email": ["This email is already in use."] } }` |
| Incorrect password (email change) | `400` | `{ "status": false, "errors": { "password": ["Incorrect password."] } }` |
| Invalid OTP (email change) | `400` | `{ "status": false, "errors": { "otp": ["Invalid OTP."] } }` |
| Unauthenticated request | `401` | Standard DRF unauthorized response |

---

## 12. Security & Business Rules

| Rule | Description |
|---|---|
| **Email Enumeration Protection** | `/forgot-password/` always returns `202`, regardless of whether email exists. |
| **Failed Login Tracking** | `user.failed_login_attempts` incremented by `1` on each wrong password (when email exists). Reset to `0` on successful login. |
| **Last Login Tracking** | `user.last_login` set to current datetime on every successful authentication. |
| **Last Password Change** | `user.last_password_change` updated after a successful password reset. |
| **OTP Rate Limiting** | Max 1 resend OTP request per user per 5 minutes. |
| **Reset Token — Single Use** | `reset_token` is invalidated after use. |
| **Email Verified At — Login OTP** | `email_verified_at` is updated when login OTP verification succeeds (`/verify-otp/`). |
| **Email Verified At — Reset OTP** | `email_verified_at` is updated when reset OTP verification succeeds (`/verify-reset-otp/`). |
| **Auto Un-verify on Forgot Password** | `is_email_verified` set to `False` when `/forgot-password/` is called with a valid email. `email_verified_at` is **not cleared** — retains previous value to indicate the account was previously verified. |
| **Time-Limited OTP** | Reset OTP expires after `RESET_OTP_EXPIRY` seconds. |
| **Time-Limited Reset Token** | `reset_token` expires after `RESET_TOKEN_EXPIRY` seconds. |
| **JWT Tokens** | Both `access` and `refresh` tokens are issued upon successful authentication. `access` token expires in **15 minutes**; `refresh` token expires in **7 days**. |
| **Token Invalidation on Password Change** | `token_invalidated_at` is updated when password is changed — all tokens issued before this timestamp are rejected. |
| **Token Invalidation on Email Change** | `token_invalidated_at` is updated when email is changed — all tokens issued before this timestamp are rejected. `password_changed_at` is also updated. |
| **Email Change OTP Throttle** | Max 1 email change OTP request per user per 3 minutes. |
| **Email Change OTP Expiry** | Email change OTP expires after `OTP_EXPIRY_TIME` (300 seconds). |
| **Pending Email** | New email is stored in `pending_email` until OTP verification succeeds. |

---

## 13. Data Models

### User Model

#### Base Fields

| Field | Type | Constraints | Description |
|---|---|---|---|
| `email` | EmailField | `unique=True` | Unique identifier and login credential |
| `password` | String (hashed) | inherited | Hashed password (Django default) |
| `first_name` | CharField | `max_length=150, blank=True` | User's first name |
| `last_name` | CharField | `max_length=150, blank=True` | User's last name |
| `gender` | CharField | `max_length=10, null=True, blank=True` | Gender — uses `Gender.choices` enum |
| `date_of_birth` | DateField | `null=True, blank=True` | User's date of birth |
| `is_active` | BooleanField | `default=True` | Account active status |
| `is_staff` | BooleanField | `default=False` | Staff/admin access flag |
| `last_login` | DateTimeField | inherited | Set to current datetime on every successful login |

#### Email Verification (OTP) Fields

| Field | Type | Constraints | Description |
|---|---|---|---|
| `otp` | CharField | `max_length=6, null=True, blank=True` | Current active OTP code (6-digit) |
| `otp_created_at` | DateTimeField | `null=True, blank=True` | Timestamp when OTP was generated; used to enforce `OTP_EXPIRY_TIME` |
| `is_email_verified` | BooleanField | `default=False` | `True` after first successful OTP verification. Reset to `False` when `/forgot-password/` is called. |
| `email_verified_at` | DateTimeField | `null=True, blank=True` | Timestamp of the most recent email verification. Updated on login OTP verify and on `/verify-reset-otp/` success. |

#### Reset Password Fields

| Field | Type | Constraints | Description |
|---|---|---|---|
| `reset_password_otp` | CharField | `max_length=6, null=True, blank=True` | OTP sent for password reset (6-digit) |
| `reset_password_otp_created_at` | DateTimeField | `null=True, blank=True` | Timestamp when reset OTP was generated; used to enforce `RESET_OTP_EXPIRY` |
| `reset_password_token` | CharField | `max_length=255, null=True, blank=True` | Secure single-use token issued after reset OTP verification |
| `reset_password_token_created_at` | DateTimeField | `null=True, blank=True` | Timestamp when reset token was issued; used to enforce `RESET_TOKEN_EXPIRY` |

#### Email Change Fields

| Field | Type | Constraints | Description |
|---|---|---|---|
| `pending_email` | EmailField | `null=True, blank=True` | Stores the new email address while awaiting OTP verification. Cleared after successful verification. |
| `email_change_otp` | CharField | `max_length=64, null=True, blank=True` | OTP sent to the new (pending) email address for verification |
| `email_change_otp_created_at` | DateTimeField | `null=True, blank=True` | Timestamp when email change OTP was generated; used to enforce `OTP_EXPIRY_TIME` |
| `email_changed_at` | DateTimeField | `null=True, blank=True` | Updated to current datetime after a successful email change |

#### Security Fields

| Field | Type | Constraints | Description |
|---|---|---|---|
| `failed_login_attempts` | IntegerField | `default=0` | Incremented on wrong password; reset to `0` on successful login |
| `account_locked_until` | DateTimeField | `null=True, blank=True` | If set, account is locked until this datetime |
| `last_password_change` | DateTimeField | `null=True, blank=True` | Updated to current datetime after successful password reset via `/reset-password/` |
| `password_changed_at` | DateTimeField | `null=True, blank=True` | Updated when password is changed via `/password/change/` or when email is changed. Used alongside `token_invalidated_at` for global logout. |
| `token_invalidated_at` | DateTimeField | `null=True, blank=True` | Updated on password or email change. Any token with `iat` before this timestamp is considered invalid — enforces global logout from all devices. |

---

## 14. API Summary Table

| # | Endpoint | Method | Purpose | Auth Required |
|---|---|---|---|---|
| 1 | `/register/` | POST | Create new user account | No |
| 2 | `/login/` | POST | Authenticate user | No |
| 3 | `/verify-otp/` | POST | Verify login OTP, receive JWT | No |
| 4 | `/resend-otp/` | POST | Resend login/verification OTP | No |
| 5 | `/forgot-password/` | POST | Request password reset OTP | No |
| 6 | `/verify-reset-otp/` | POST | Verify reset OTP, receive reset_token | No |
| 7 | `/reset-password/` | POST | Set new password using reset_token | No |
| 8 | `/refresh/` | POST | Get new access token using refresh token | No |
| 9 | `/password/change/` | PUT | Change password (invalidates all tokens) | **Yes** |
| 10 | `/email/change/` | POST | Request email change OTP to new email | **Yes** |
| 11 | `/email/change/verify/` | POST | Verify OTP and apply new email (invalidates all tokens) | **Yes** |

---

*Document prepared based on API specification and observed request/response behavior.*