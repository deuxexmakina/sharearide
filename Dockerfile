# Use Nginx image from Docker Hub
FROM nginx:latest

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy local folder to nginx website folder
COPY ./www /usr/share/nginx/html

# Copy configuration file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080
EXPOSE 8080

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
