# Use a lightweight web server for serving static files
FROM nginx:alpine

# Copy the static files to the nginx server
COPY . /usr/share/nginx/html

# Expose the port that Nginx listens on
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
