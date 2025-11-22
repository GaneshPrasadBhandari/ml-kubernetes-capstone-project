# Use official Nginx image
FROM nginx:alpine

# Remove default Nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy our static site
COPY index.html /usr/share/nginx/html/index.html

# Nginx listens on port 80
EXPOSE 80

# Use default nginx start command
CMD ["nginx", "-g", "daemon off;"]
