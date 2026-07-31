import os

# Define the templates to create
templates = {
    'templates/base.html': '<h1>This is the Base Template</h1>',
    'templates/dashboard.html': '<h1>This is the Main Dashboard</h1>',
    
    'apps/accounts/templates/accounts/login.html': '<h1>This is the Login Page</h1>',
    'apps/accounts/templates/accounts/signup.html': '<h1>This is the Sign Up Page</h1>',
    'apps/accounts/templates/accounts/verify_email.html': '<h1>This is the Verify Email Page</h1>',
    
    'apps/organizations/templates/organizations/create_org.html': '<h1>This is the Create Organization Page</h1>',
    'apps/organizations/templates/organizations/org_settings.html': '<h1>This is the Organization Settings Page</h1>',
    'apps/organizations/templates/organizations/team_management.html': '<h1>This is the Team Management Page</h1>',
    'apps/organizations/templates/organizations/billing.html': '<h1>This is the Billing Page</h1>',
    
    'apps/projects/templates/projects/project_list.html': '<h1>This is the Projects Dashboard</h1>',
    'apps/projects/templates/projects/project_create.html': '<h1>This is the Create Project Page</h1>',
    'apps/projects/templates/projects/project_detail.html': '<h1>This is the Project Details Page</h1>',
    
    'apps/tasks/templates/tasks/task_list.html': '<h1>This is the Tasks Dashboard</h1>',
    'apps/tasks/templates/tasks/task_create.html': '<h1>This is the Create Task Page</h1>',
    'apps/tasks/templates/tasks/task_detail.html': '<h1>This is the Task Details Page</h1>',
    
    'apps/documents/templates/documents/document_list.html': '<h1>This is the Documents Page</h1>',
}

# Create directories and files
for filepath, content in templates.items():
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Scaffolding complete!")
