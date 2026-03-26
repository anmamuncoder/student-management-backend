URL_PERMISSION_MAP = [ 
    (r'/api/v1/accounts/users/','user'),
    
    # Self acc/accountsount actions (standard naming)
    (r'/api/v1/accounts/password/change/', 'self_account'), # - PUT
    (r'/api/v1/accounts/email/change/', 'self_account'), # POST
    (r'/api/v1/accounts/email/change/verify/', 'self_account'), # POST
]

HTTP_METHOD_ACTION_MAP = {
    'GET':'view',
    'POST':'create',
    'PUT':'update',
    'PATCH':'update',
    'DELETE':'delete',
    'HEAD':'view',
    'OPTIONS':'None',
}

EXEMPT_PATHS = [
    # Its Unauthenticated API'S
    r'^/api/v1/accounts/register/',
    r'^/api/v1/accounts/login/',
    r'^/api/v1/accounts/verify-otp/',
    r'^/api/v1/accounts/resend-otp/',
    r'^/api/v1/accounts/forgot-password/',
    r'^/api/v1/accounts/verify-reset-otp/',
    r'^/api/v1/accounts/reset-password/',
    r'^/api/v1/accounts/refresh/',

    
    r'^/admin/',
    r'^/api/schema/',
    r'^/api/docs/',
    r'^/api/redoc/',
    # r'^/health/',
]

# That will be create with for custom
# python manage.py setup_rbac 
# python manage.py setup_rbac --reset-roles True/False

# ------------ INITIAL SEED DATA ---------------
INITIAL_PERMISSIONS = [
    # Products
    {'name': 'View product',    'resource': 'product',   'action': 'view',   'slug': 'product:view'},
    {'name': 'Create product',  'resource': 'product',   'action': 'create', 'slug': 'product:create'},
    {'name': 'Update product',  'resource': 'product',   'action': 'update', 'slug': 'product:update'},
    {'name': 'Delete product',  'resource': 'product',   'action': 'delete', 'slug': 'product:delete'},

    # Orders
    {'name': 'View order',      'resource': 'order',     'action': 'view',   'slug': 'order:view'},
    {'name': 'Create order',    'resource': 'order',     'action': 'create', 'slug': 'order:create'},
    {'name': 'Update order',    'resource': 'order',     'action': 'update', 'slug': 'order:update'},
    {'name': 'Delete order',    'resource': 'order',     'action': 'delete', 'slug': 'order:delete'},
    
    # Users
    {'name': 'View user',       'resource': 'user',      'action': 'view',   'slug': 'user:view'},
    {'name': 'Create user',     'resource': 'user',      'action': 'create', 'slug': 'user:create'},
    {'name': 'Update user',     'resource': 'user',      'action': 'update', 'slug': 'user:update'},
    {'name': 'Delete user',     'resource': 'user',      'action': 'delete', 'slug': 'user:delete'},

    # Self Account (single permission)
    {'name': 'Update own account', 'resource': 'self_account', 'action': 'update', 'slug': 'self_account:update'},
    {'name': 'Update own account', 'resource': 'self_account', 'action': 'create', 'slug': 'self_account:create'},
]

# -------------------------------
# INITIAL ROLES
# -------------------------------
# permission.slug list 

# Never create a separate 'Admin' role because superusers are already treated as admins.
# Define initial roles and their associated permissions.

INITIAL_ROLES = {
    # Viewer: read-only access
    'viewer': [
        'product:view',
        'order:view',
        'user:view',  
        'self_account:update','self_account:create'  # allows user to update own account
    ],

    # Editor: can create and update operational resources
    'editor': [
        'product:view', 'product:create', 'product:update',
        'order:view',   'order:create',   'order:update',
        'user:view',  # optional
        'self_account:update', 'self_account:create',  # always allow self-account changes
    ],

    # Manager: full CRUD on operational resources (but no admin/user management)
    'manager': [
        'product:view','product:create','product:update','product:delete',
        'order:view','order:create','order:update','order:delete',
        'user:view',  # managers can view users
        'self_account:update', 'self_account:create',  # self-account actions for all users
    ],
    # superusers bypass RBAC, no separate admin role
}
