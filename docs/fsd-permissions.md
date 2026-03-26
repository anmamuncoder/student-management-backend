##### Functional Specification Document (FSD)
## Role-Based Access Control (RBAC) System

**Project:** User Authentication System
**Module:** `apps.rbac`
**Version:** 1.0
**Date:** 2026-03-24

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Configuration](#3-configuration)
   - 3.1 [URL Permission Map](#31-url-permission-map)
   - 3.2 [HTTP Method Action Map](#32-http-method-action-map)
   - 3.3 [Exempt Paths](#33-exempt-paths)
   - 3.4 [Initial Seed Data](#34-initial-seed-data)
4. [Middleware Flow](#4-middleware-flow)
5. [Permission Resolution](#5-permission-resolution)
6. [Caching](#6-caching)
7. [Management Command](#7-management-command)
8. [API Endpoints](#8-api-endpoints)
   - 8.1 [Permissions API](#81-permissions-api)
   - 8.2 [Self Permissions API](#82-self-permissions-api)
   - 8.3 [Roles API](#83-roles-api)
   - 8.4 [User Roles API](#84-user-roles-assign-api)
   - 8.5 [RBAC API Access Summary](#85-rbac-api-access-summary)
9. [Utility Functions](#9-utility-functions)
10. [Security & Business Rules](#10-security--business-rules)
11. [Data Models](#11-data-models)
12. [Error Responses](#12-error-responses)

---

## 1. Overview

This document describes the complete functional specification of the Role-Based Access Control (RBAC) system. The system controls access to API resources based on user roles and permissions, enforced at the middleware level using JWT authentication.

Initial permissions and roles are seeded once via the `setup_rbac` management command from hardcoded config data (`INITIAL_PERMISSIONS` and `INITIAL_ROLES` in `config.py`). After seeding, permissions are **immutable** — they cannot be created, updated, or deleted through the API. Roles are created and managed exclusively by superusers through the admin API. User-role assignments are also managed by superusers only.

---

### Feature List

#### 🛡️ Access Control

| # | Feature | Description |
|---|---|---|
| 1 | **Middleware-Based RBAC** | Permission checks are enforced in `RBACMiddleware` before any view is reached. |
| 2 | **JWT-Integrated Auth** | Middleware authenticates the user via JWT on every non-exempt request. |
| 3 | **Superuser Bypass** | `is_superuser = True` users pass all permission checks automatically — no role required. |
| 4 | **Resource-Action Permission Model** | Permissions are expressed as `resource:action` slugs (e.g., `product:view`, `order:delete`). |
| 5 | **URL-to-Resource Mapping** | API paths are mapped to resource names via `URL_PERMISSION_MAP` using regex matching. |
| 6 | **HTTP Method-to-Action Mapping** | HTTP methods are mapped to actions: `GET→view`, `POST→create`, `PUT/PATCH→update`, `DELETE→delete`. |
| 7 | **Exempt Path Support** | Certain paths (login, register, docs, admin) are whitelisted and bypass all RBAC checks. |
| 8 | **CORS Preflight Bypass** | `OPTIONS` requests always pass through without permission checks. |

#### 👥 Role Management

| # | Feature | Description |
|---|---|---|
| 9 | **Named Roles** | Roles group multiple permissions together (e.g., `viewer`, `editor`, `manager`). |
| 10 | **Many-to-Many Role-Permission** | A role can have many permissions; a permission can belong to many roles. |
| 11 | **Many Roles per User** | A user can be assigned multiple roles simultaneously via `UserRole`. |
| 12 | **No Separate Admin Role** | Superusers are treated as admins — no `admin` role is needed or created. |
| 13 | **Admin-Only Role Management** | Roles can only be created, updated, or deleted by superusers via the API. |
| 14 | **Admin-Only User-Role Assignment** | User-role assignments are managed exclusively by superusers via the API. |

#### ⚡ Performance

| # | Feature | Description |
|---|---|---|
| 15 | **Permission Caching** | User permissions are cached per-user for 5 minutes to avoid repeated DB queries on every request. |
| 16 | **Cache Invalidation on Role Change** | Cache is cleared when a user's role is updated. |
| 17 | **Cache Invalidation on Permission Change** | Cache is cleared for all users of a role when the role's permissions are updated. |

#### 🔧 Setup & Seeding

| # | Feature | Description |
|---|---|---|
| 18 | **Management Command** | `python manage.py setup_rbac` seeds `INITIAL_PERMISSIONS` and `INITIAL_ROLES` from `config.py`. |
| 19 | **Idempotent Seeding** | Re-running the command does not duplicate data — uses `get_or_create`. |
| 20 | **Role Reset Flag** | `--reset-roles True/False` re-syncs role permissions from config without affecting user assignments. |
| 21 | **Immutable Permissions** | Permissions are fixed after seeding. No API endpoint allows creating, updating, or deleting them. |

---

## 2. Architecture

```
HTTP Request
     │
     ▼
RBACMiddleware
     │
     ├── 1. Exempt path?          → pass through
     ├── 2. Not /api/ route?      → pass through
     ├── 3. OPTIONS method?       → pass through
     ├── 4. JWT authenticate      → 401 if failed
     ├── 5. is_superuser?         → pass through
     ├── 6. URL → resource        → pass through if no match
     ├── 7. HTTP method → action  → pass through if no match
     ├── 8. Build slug            → "resource:action"
     ├── 9. Check user perms      → 403 if not found
     └── 10. Set request.user     → pass through to view
```

---

## 3. Configuration

### 3.1 URL Permission Map

Maps API URL patterns (regex) to resource names. Matched top-to-bottom — first match wins.

```python
URL_PERMISSION_MAP = [
    (r'/api/v1/products/',          'product'),
    # (r'/api/v1/orders/',          'order'),       # commented out — inactive
    (r'/api/v1/users/',             'user'),
    (r'/api/v1/categories/',        'categories'),
    (r'/api/v1/reports/',           'reports'),
    (r'/api/v1/inventory/',         'inventory'),
    (f'/api/v1/accounts/tesing/',   'order'),       # custom mapping for order resource
]
```

| URL Pattern | Resource Name | Status |
|---|---|---|
| `/api/v1/products/*` | `product` | Active |
| `/api/v1/orders/*` | `order` | Commented out (inactive) |
| `/api/v1/users/*` | `user` | Active |
| `/api/v1/categories/*` | `categories` | Active |
| `/api/v1/reports/*` | `reports` | Active |
| `/api/v1/inventory/*` | `inventory` | Active |
| `/api/v1/accounts/tesing/*` | `order` | Active (custom mapping) |

> If no pattern matches the request path, the middleware passes the request through without a permission check.

---

### 3.2 HTTP Method Action Map

Maps HTTP methods to permission action names.

```python
HTTP_METHOD_ACTION_MAP = {
    'GET':     'view',
    'POST':    'create',
    'PUT':     'update',
    'PATCH':   'update',
    'DELETE':  'delete',
    'HEAD':    'view',
    'OPTIONS': 'None',   # Always exempt — CORS preflight
}
```

| HTTP Method | Action | Notes |
|---|---|---|
| `GET` | `view` | |
| `POST` | `create` | |
| `PUT` | `update` | |
| `PATCH` | `update` | Same as PUT |
| `DELETE` | `delete` | |
| `HEAD` | `view` | Same as GET |
| `OPTIONS` | `None` | Always exempt (CORS preflight) |

---

### 3.3 Exempt Paths

Paths that bypass all RBAC and JWT checks entirely. Matched using regex.

```python
EXEMPT_PATHS = [
    r'^/api/v1/accounts/login/',
    r'^/api/v1/accounts/logout/',
    r'^/api/v1/accounts/refresh/',
    r'^/api/v1/auth/register/',
    r'^/api/v1/auth/password/',
    r'^/admin/',
    r'^/api/schema/',
    r'^/api/docs/',
    r'^/api/redoc/',
    r'^/health/',
]
```

| Exempt Path Pattern | Reason |
|---|---|
| `^/api/v1/accounts/login/` | Public — login endpoint |
| `^/api/v1/accounts/logout/` | Public — logout endpoint |
| `^/api/v1/accounts/refresh/` | Public — token refresh |
| `^/api/v1/auth/register/` | Public — registration |
| `^/api/v1/auth/password/` | Public — password reset |
| `^/admin/` | Django admin — has its own auth |
| `^/api/schema/` | API schema docs |
| `^/api/docs/` | Swagger UI |
| `^/api/redoc/` | ReDoc UI |
| `^/health/` | Health check endpoint |

---

### 3.4 Initial Seed Data

All seed data is defined in `config.py` and applied once via `python manage.py setup_rbac`. This data is the source of truth for all permissions in the system. Permissions cannot be changed after seeding except via the management command.

#### Initial Permissions (`INITIAL_PERMISSIONS`)

```python
INITIAL_PERMISSIONS = [
    # Products
    {'name': 'View product',   'slug': 'product:view',   'resource': 'product', 'action': 'view'},
    {'name': 'Create product', 'slug': 'product:create', 'resource': 'product', 'action': 'create'},
    {'name': 'Update product', 'slug': 'product:update', 'resource': 'product', 'action': 'update'},
    {'name': 'Delete product', 'slug': 'product:delete', 'resource': 'product', 'action': 'delete'},
    # Orders
    {'name': 'View order',     'slug': 'order:view',     'resource': 'order',   'action': 'view'},
    {'name': 'Create order',   'slug': 'order:create',   'resource': 'order',   'action': 'create'},
    {'name': 'Update order',   'slug': 'order:update',   'resource': 'order',   'action': 'update'},
    {'name': 'Delete order',   'slug': 'order:delete',   'resource': 'order',   'action': 'delete'},
    # Users
    {'name': 'View user',      'slug': 'user:view',      'resource': 'user',    'action': 'view'},
    {'name': 'Create user',    'slug': 'user:create',    'resource': 'user',    'action': 'create'},
    {'name': 'Update user',    'slug': 'user:update',    'resource': 'user',    'action': 'update'},
    {'name': 'Delete user',    'slug': 'user:delete',    'resource': 'user',    'action': 'delete'},
]
```

| Slug | Resource | Action |
|---|---|---|
| `product:view` | product | view |
| `product:create` | product | create |
| `product:update` | product | update |
| `product:delete` | product | delete |
| `order:view` | order | view |
| `order:create` | order | create |
| `order:update` | order | update |
| `order:delete` | order | delete |
| `user:view` | user | view |
| `user:create` | user | create |
| `user:update` | user | update |
| `user:delete` | user | delete |

#### Initial Roles (`INITIAL_ROLES`)

```python
INITIAL_ROLES = {
    'viewer': [
        'product:view', 'order:view', 'category:view', 'report:view',
    ],
    'editor': [
        'product:view', 'product:create', 'product:update',
        'order:view',   'order:create',   'order:update',
        'category:view','category:create','category:update',
    ],
    'manager': [
        'product:view', 'product:create', 'product:update', 'product:delete',
        'order:view',   'order:create',   'order:update',   'order:delete',
        'category:view','category:create','category:update','category:delete',
        'report:view',  'report:create',
        'user:view',
    ],
    # 'admin' role is intentionally excluded.
    # Superusers (is_superuser=True) have full access without a role.
}
```

| Role | Permissions |
|---|---|
| `viewer` | `product:view`, `order:view`, `category:view`, `report:view` |
| `editor` | `product:view/create/update`, `order:view/create/update`, `category:view/create/update` |
| `manager` | `product:view/create/update/delete`, `order:view/create/update/delete`, `category:view/create/update/delete`, `report:view/create`, `user:view` |

> **No `admin` role is defined.** Superusers (`is_superuser = True`) automatically have full access and do not need a role.

> After initial seeding, additional roles can be created via the Roles API by superusers. The `INITIAL_ROLES` in config represent the baseline only.

---

## 4. Middleware Flow

### `RBACMiddleware` — Step-by-Step

#### Step 1 — Exempt Path Check
- If the request path matches any pattern in `EXEMPT_PATHS` → pass through immediately.

#### Step 2 — API Route Filter
- If path does not start with `/api/` → pass through (non-API routes are not managed by RBAC).

#### Step 3 — OPTIONS Bypass
- If HTTP method is `OPTIONS` → pass through (CORS preflight must not be blocked).

#### Step 4 — JWT Authentication
- Calls `JWTAuthentication().authenticate(request)`.
- If token is missing, invalid, or expired → returns `401`.
- On success → `user` object is extracted from the token.

#### Step 5 — Superuser Bypass
- If `user.is_superuser == True` → set `request.user = user` and pass through.

#### Step 6 — URL to Resource Mapping
- Calls `_get_resource_from_path(path)` using `URL_PERMISSION_MAP`.
- If no match → set `request.user = user` and pass through (unmanaged resource).

#### Step 7 — HTTP Method to Action Mapping
- Looks up `HTTP_METHOD_ACTION_MAP.get(method)`.
- If no match → set `request.user = user` and pass through.

#### Step 8 — Permission Slug Construction
- Builds the required permission string: `f"{resource}:{action}"`.
- Example: `GET /api/v1/products/` → `"product:view"`.

#### Step 9 — Permission Check
- Calls `get_user_permissions(user)` (cached for 5 minutes).
- If required slug not in user's permissions → returns `403` with details.
- Logs a warning with user ID, required permission, path, and method.

#### Step 10 — Pass Through
- Sets `request.user = user` and passes to the view.

---

## 5. Permission Resolution

A user's effective permissions are the union of all permissions from all roles assigned to them.

```
User
 └── UserRole (M2M)
      └── Role
           └── Permission (M2M)
                └── slug: "product:view"
```

**Query:**
```python
Permission.objects.filter(roles__user_roles__user=user).values_list('slug', flat=True)
```

Result is a `set` of slugs, e.g.: `{"product:view", "order:create", "user:view"}`

---

## 6. Caching

| Property | Value |
|---|---|
| Cache key format | `rbac:user_perms:{user.id}` |
| Cache duration | 300 seconds (5 minutes) |
| Cache backend | Django default cache (configured in settings) |

### Cache Invalidation Triggers

| Trigger | Function Called | Effect |
|---|---|---|
| User's role is changed | `clear_user_permission_cache(user_id)` | Clears cache for that specific user |
| Role's permissions are updated | `clear_role_permission_cache(role)` | Clears cache for all users assigned to that role |

---

## 7. Management Command

### `python manage.py setup_rbac`

Seeds `INITIAL_PERMISSIONS` and `INITIAL_ROLES` from `config.py` into the database. This is the **only** mechanism by which permissions are created in the system.

#### Arguments

| Argument | Type | Description |
|---|---|---|
| *(none)* | — | Seeds all permissions and roles from config. Skips already-existing records. |
| `--reset-roles` | `True` / `False` | Re-syncs all role permissions from config. Does not affect user-role assignments. |

#### Behavior

**Step 1 — Create Permissions**
- Iterates over `INITIAL_PERMISSIONS`.
- Uses `get_or_create(slug=...)` — existing permissions are never duplicated.
- Reports count of newly created vs already existing.

**Step 2 — Create Roles & Assign Permissions**
- Iterates over `INITIAL_ROLES`.
- Uses `get_or_create(slug=...)` for each role.
- If role is newly created OR `--reset-roles True` is passed → calls `role.permissions.set(perms)`.
- If role already exists and `--reset-roles` is not passed → skips (no change).
- Warns if any permission slug in config does not exist in the database.

#### Example Usage

```bash
# Initial setup — seeds all permissions and roles
python manage.py setup_rbac

# Re-sync role permissions after config change
python manage.py setup_rbac --reset-roles True
```


---

<br>
<br>


## 8. API Endpoints

All RBAC endpoints require the user to be a superuser (`IsAdminUser`). A JWT token must be provided in the `Authorization: Bearer <token>` header.

---

### 8.1 Permissions API

Base URL: `/api/v1/rbac/permissions/`

Permissions are **read-only** via the API. They are seeded once by `setup_rbac` and cannot be created, modified, or deleted through any endpoint.

| Method | URL | Description | Access |
|---|---|---|---|
| `GET` | `/api/v1/rbac/permissions/` | List all permissions | Superuser only |
| `GET` | `/api/v1/rbac/permissions/{slug}/` | Retrieve a single permission | Superuser only |


> `POST`, `PUT`, `PATCH`, and `DELETE` are **not available** for permissions.

#### Lookup Field
Permissions are retrieved by their `slug` (e.g., `order:delete`).

#### Permission Object

```json
{
  "id": "3096301b-5f43-42aa-9ea0-89966c239f1d",
  "name": "Delete order",
  "description": "Allows deletion of order records via the `/api/v1/orders/` API endpoint.",

  "resource": "order",
  "action": "delete",
  "slug": "order:delete",

  "created_at": "2026-03-23T00:12:47.258577+06:00",
  "updated_at": "2026-03-24T15:25:03.821205+06:00"
}
```

---

### 8.2 Self Permissions API

Base URL: `/api/v1/rbac/permissions/self/`

Allows any authenticated user to view their own permissions, grouped by role. No superuser privilege is required — any valid JWT token grants access to this endpoint.

| Method | URL | Description | Access |
|---|---|---|---|
| `GET` | `/api/v1/rbac/permissions/self/` | Retrieve the current user's permissions grouped by role | Any authenticated user |

#### Response

Permissions are returned as a dictionary keyed by role slug, with each value being the list of permission slugs assigned to that role.

```json
{
  "success": true,
  "message": "Permissions retrieved successfully.",
  "data": {
    "viewer": [
      "order:view", 
      "product:view", 
      "self_account:update"
    ],
    "editor": [
      "product:create", 
      "product:update"
    ]
  }
}
```

#### Notes
- The response reflects only the roles currently assigned to the authenticated user.
- If a user has no roles assigned, `data` will be an empty object `{}`.
- Superusers calling this endpoint will see their assigned roles (if any). Their full access comes from `is_superuser`, not from the permissions listed here.
- This endpoint is exempt from RBAC middleware permission checks — it only requires a valid JWT token.

---

### 8.3 Roles API

Base URL: `/api/v1/rbac/roles/`

Roles are fully managed via the API by superusers. When assigning permissions to a role, only slugs that exist in `INITIAL_PERMISSIONS` (seeded by `setup_rbac`) are valid.

| Method | URL | Description | Access |
|---|---|---|---|
| `GET` | `/api/v1/rbac/roles/` | List all roles | Superuser only |
| `POST` | `/api/v1/rbac/roles/` | Create a new role | Superuser only |
| `GET` | `/api/v1/rbac/roles/{slug}/` | Retrieve a role | Superuser only |
| `PUT` | `/api/v1/rbac/roles/{slug}/` | Full update of a role | Superuser only |
| `PATCH` | `/api/v1/rbac/roles/{slug}/` | Partial update of a role | Superuser only |
| `DELETE` | `/api/v1/rbac/roles/{slug}/` | Delete a role | Superuser only |

#### Create Role — Request Body

```json
{
  "name": "Editor",
  "description": "Allows product updates with read-only access to orders and users.",
  "permissions": [
    "order:view", 
    "product:update",
    "product:view",
    "user:view"
  ]
}
```

#### Role Object Response

```json
{
  "id": "71b00eaa-526f-48bc-be0e-795fe2194930",
  "name": "Editor",
  "slug": "editor",
  "permissions": [
    "order:create",
    "product:create", 
    "product:update",
    "product:view"
  ],
  "description": "Allows product updates with read-only access to orders and users.",
  "created_at": "2026-03-23T00:12:47.290573+06:00",
  "updated_at": "2026-03-24T01:33:34.241815+06:00"
}
```

#### Notes
- `slug` is auto-generated from `name` via `slugify` and is **read-only**.
- `permissions` accepts a list of existing permission slugs only. Any slug not found in the database returns a validation error.
- Lookup field is `slug` (e.g., `/api/v1/rbac/roles/editor/`).
- Updating a role's permissions via `PUT`/`PATCH` automatically clears the permission cache for all users assigned to that role.

---

### 8.4 User Roles Assign API

Base URL: `/api/v1/rbac/user-roles-assign/`

Manages assignment of roles to users. Only superusers can manage user-role assignments.

| Method | URL | Description | Access |
|---|---|---|---|
| `GET` | `/api/v1/rbac/user-roles-assign/` | List all user-role assignments | Superuser only |
| `POST` | `/api/v1/rbac/user-roles-assign/` | Assign a role to a user | Superuser only |
| `GET` | `/api/v1/rbac/user-roles-assign/{id}/` | Retrieve a specific assignment | Superuser only |
| `PATCH` | `/api/v1/rbac/user-roles-assign/{id}/` | Update a user's role assignment | Superuser only |
| `DELETE` | `/api/v1/rbac/user-roles-assign/{id}/` | Remove a user-role assignment | Superuser only |

#### Assign Role — Request Body

```json
{
  "user": "user@example.com",
  "role": "editor"
}
```

#### Update Role Assignment — Request Body

```json
{
  "role": "manager"
}
```

#### User Role Object Response

```json
{
  "id": "ae6ecf0d-3a7d-4b56-bcfc-0beff9255ac6",
  "user": "user@example.com",
  "role": "editor"
}
```

#### Notes
- `user` is referenced by **email**.
- `role` is referenced by **slug**.
- A user cannot be assigned the same role twice (`unique_together = ['user', 'role']`).
- Updating a user-role assignment via `PATCH` automatically clears that user's permission cache.

<br>

### 8.5 RBAC API Access Summary

| Endpoint | Method | Access | Description |
|---|---|---|---|
| `/api/v1/rbac/permissions/self/` | `GET` | Any authenticated user (normal + admin) | View own permissions grouped by role |
| `/api/v1/rbac/permissions/` | `GET` | Admin (superuser) only | List all permissions in the system |
| `/api/v1/rbac/permissions/{slug}/` | `GET` | Admin (superuser) only | Retrieve a single permission |
| `/api/v1/rbac/roles/` | `GET` `POST` | Admin (superuser) only | List all roles / Create a new role |
| `/api/v1/rbac/roles/{slug}/` | `GET` `PUT` `PATCH` `DELETE` | Admin (superuser) only | Retrieve / Update / Delete a role |
| `/api/v1/rbac/user-roles-assign/` | `GET` `POST` | Admin (superuser) only | List all assignments / Assign role to user |
| `/api/v1/rbac/user-roles-assign/{id}/` | `GET` `PATCH` `DELETE` | Admin (superuser) only | Retrieve / Update / Remove a user-role assignment |


---

<br>
<br>


## 9. Utility Functions

All functions are in `apps/rbac/utils.py`.

<h6>

| Function | Signature | Description |
|---|---|---|
| `_get_resource_from_path` | `(path: str) → str \| None` | Matches URL path against `URL_PERMISSION_MAP`, returns resource name or `None`. |
| `_is_exempt` | `(path: str) → bool` | Returns `True` if path matches any pattern in `EXEMPT_PATHS`. |
| `get_user_permissions` | `(user) → set` | Returns set of permission slugs for user. Results cached for 5 minutes. |
| `clear_user_permission_cache` | `(user_id: int)` | Deletes cached permissions for a specific user. |
| `clear_role_permission_cache` | `(role)` | Deletes cached permissions for all users assigned to the given role. |
| `user_has_permission` | `(user, perm_slug: str) → bool` | Returns `True` if user has the given permission slug. Superuser always returns `True`. |
| `user_has_any_permission` | `(user, perm_slugs: list) → bool` | Returns `True` if user has at least one of the given slugs. |
| `user_has_all_permissions` | `(user, perm_slugs: list) → bool` | Returns `True` only if user has all of the given slugs. |

</h6>


---

## 10. Security & Business Rules

<h6>

| Rule | Description |
|---|---|
| **Superuser Full Access** | `is_superuser = True` bypasses all permission checks. No role assignment needed. |
| **No Admin Role** | Admin-level access is achieved solely through `is_superuser`. No `admin` role exists to prevent privilege escalation via role assignment. |
| **Immutable Permissions** | Permissions are seeded once by `setup_rbac` and are fixed. No API endpoint allows creating, updating, or deleting permissions. |
| **Admin-Only Role Management** | Only superusers (`IsAdminUser`) can create, update, or delete roles via the API. |
| **Admin-Only User-Role Management** | Only superusers can assign or remove roles from users. |
| **Slug Uniqueness** | Permission slugs are unique across the system (`unique=True`). Auto-generated as `resource:action`. |
| **Unmatched URL Passthrough** | If a URL does not match any entry in `URL_PERMISSION_MAP`, the request passes through without a permission check. Add URLs to the map to protect them. |
| **Unmatched Method Passthrough** | If an HTTP method has no mapping in `HTTP_METHOD_ACTION_MAP`, the request passes through. |
| **Cache Consistency** | Permission cache must be invalidated whenever roles or user-role assignments are changed to prevent stale access. |
| **Transaction Safety** | `setup_rbac` wraps all DB operations in `@transaction.atomic` — partial seeds are rolled back on failure. |
| **Missing Permission Warning** | If a role in `INITIAL_ROLES` references a slug that doesn't exist in the DB, a warning is printed during `setup_rbac` without raising an error. |

</h6>


---

<br>
<br>


## 11. Data Models

### Permission

| Field | Type | Constraints | Description |
|---|---|---|---|
| `name` | CharField | `max_length=100` | Human-readable name (e.g., `"View product"`) |
| `slug` | SlugField | `max_length=100, unique=True, db_index=True` | Auto-generated as `resource:action` (e.g., `product:view`) |
| `resource` | CharField | `max_length=50` | Resource name (e.g., `product`, `order`) |
| `action` | CharField | `max_length=50` | Action name (e.g., `view`, `create`, `update`, `delete`) |
| `description` | TextField | `blank=True` | Optional description |

- `unique_together = ['resource', 'action']`
- `ordering = ['resource', 'action']`
- `slug` is auto-generated on `save()` as `f"{resource}:{action}".lower()`

---

### Role

| Field | Type | Constraints | Description |
|---|---|---|---|
| `name` | CharField | `max_length=100, unique=True` | Role name (e.g., `viewer`, `editor`, `manager`) |
| `slug` | SlugField | `max_length=100, unique=True, db_index=True` | Auto-generated from `name` via `slugify` |
| `permissions` | ManyToManyField | `→ Permission, blank=True` | Permissions assigned to this role |
| `description` | TextField | `blank=True` | Optional description |
| `created_at` | DateTimeField | `auto_now_add=True` | Creation timestamp |
| `updated_at` | DateTimeField | `auto_now=True` | Last update timestamp |

- `ordering = ['name']`
- `slug` is auto-generated on `save()` via `slugify(name)`

---

### UserRole

| Field | Type | Constraints | Description |
|---|---|---|---|
| `user` | ForeignKey | `→ User, CASCADE` | The user being assigned a role |
| `role` | ForeignKey | `→ Role, CASCADE` | The role being assigned |

- `unique_together = ['user', 'role']` — a user cannot be assigned the same role twice
- Extends `AuditModel` (created_by, updated_by tracking)

---

<br>
<br>

## 12. Error Responses

### 401 — Unauthenticated

Returned when JWT token is missing, invalid, or expired.

```json
{
  "status": false,
  "errors": {
    "message": "Authentication credentials were not provided or are invalid."
  }
}
```

### 403 — Permission Denied

Returned when the authenticated user lacks the required permission.

```json
{
  "status": false,
  "errors": {
    "message": "You do not have permission to perform this action.",
    "required_permission": "order:view",
    "your_permissions": [
      "order:create",
      "product:create",
      "product:update",
      "product:view"
    ]
  }
}
```

### 400 — Validation Error (Invalid Permission Slug)

Returned when a role is created or updated with a permission slug that does not exist in the database.

```json
{
  "status": false,
  "errors": {
    "permissions": [
      "Object with slug=nonexistent:action does not exist."
    ]
  }
}
```

### 400 — Validation Error (User Not Found)

Returned when assigning a role to a user email that does not exist.

```json
{
  "status": false,
  "errors": {
    "user": [
      "Object with email=unknown@example.com does not exist."
    ]
  }
}
```

---

*Document prepared based on `apps/rbac` source code — `middleware.py`, `config.py`, `utils.py`, `models.py`, `serializers.py`, `views.py`, and `management/commands/setup_rbac.py`.*