# Use official OpenJDK 17 runtime as a parent image
FROM eclipse-temurin:17-jdk-jammy

# Set working directory in the container
WORKDIR /app

# Copy the packaged jar file from the target directory
COPY target/orderservice-0.0.1-SNAPSHOT.jar orderservice.jar

# Expose the port the app runs on
EXPOSE 8080

# Run the jar file
ENTRYPOINT ["java", "-jar", "orderservice.jar"]
