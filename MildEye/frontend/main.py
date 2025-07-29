# frontend/main.py
from fasthtml.common import *

# Initialize the app and router with live reloading for development
app, rt = fast_app(live=True)

# Define the home page route using the router (rt) directly as a decorator
@rt("/") # Corrected: Removed .get(), use rt directly for GET routes
def home():
    return Title("MildEye - Your Personal AI Platform"), Body(
        Div(
            H1("Welcome to MildEye!"),
            P("Your personal AI platform for residual passive income and skill showcase."),
            P("This is the beginning of your journey. We're building this step-by-step."),
            Button("Learn More", onclick="alert('More features coming soon!');"),
            _class="container p-4 text-center"
        ),
        # Basic Tailwind CSS classes for styling (you'll need to link Tailwind or a custom CSS later)
        _class="min-h-screen flex items-center justify-center bg-gray-100"
    )

if __name__ == "__main__":
    serve()