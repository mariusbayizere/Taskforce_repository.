# from app import create_app
# import os


# print(os.path.abspath(__file__))

# app = create_app()


# if __name__ == '__main__':
#     # app = create_app()
#     app.run(debug=True)


from app import create_app
import os
print(os.path.abspath(__file__))

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Use the PORT from the environment variable (default to 5000 if not set)
    port = int(os.getenv("PORT", 5000))
    
    # Bind the app to 0.0.0.0 to ensure it listens on all network interfaces
    app.run(host="0.0.0.0", port=port, debug=True)
