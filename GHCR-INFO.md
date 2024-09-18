# Using GitHub Container Registry (GHCR) for Our Project

GitHub Container Registry (GHCR) is a container registry service provided by GitHub. It allows you to host and manage Docker container images within your GitHub account or organization. This is an excellent choice for our open-source Kubernetes-Driven Digital Aquarium project for several reasons:

1. **Integration with GitHub**: GHCR is tightly integrated with GitHub, making it easy to manage access and permissions using your existing GitHub account.

2. **Free for public repositories**: For open-source projects, GHCR is free to use with unlimited bandwidth and storage for public images.

3. **Support for Docker and OCI images**: GHCR supports both Docker and OCI (Open Container Initiative) images.

4. **Fine-grained permissions**: You can control who can pull, push, and manage your container images.

5. **GitHub Actions integration**: Easily build and push images to GHCR as part of your CI/CD workflow using GitHub Actions.

## How to Use GHCR for Our Project

1. **Enable improved container support**:
   - Go to your GitHub account settings
   - Navigate to "Features" under your account or organization
   - Enable "Improved container support"

2. **Authenticate to GHCR**:
   - Create a personal access token (PAT) with the appropriate scopes (`read:packages`, `write:packages`, `delete:packages`)
   - Use this token to log in to GHCR:
     ```
     echo $PAT | docker login ghcr.io -u USERNAME --password-stdin
     ```

3. **Build and push your image**:
   ```
   docker build -t ghcr.io/USERNAME/fish-microservice:latest .
   docker push ghcr.io/USERNAME/fish-microservice:latest
   ```

4. **Update Kubernetes manifests**:
   In your Kubernetes deployment files, update the image reference to use GHCR:
   ```yaml
   image: ghcr.io/USERNAME/fish-microservice:latest
   ```

5. **Set up GitHub Actions**:
   Create a workflow file (e.g., `.github/workflows/build-push.yml`) to automate building and pushing your image:

   ```yaml
   name: Build and Push to GHCR

   on:
     push:
       branches: [ main ]

   jobs:
     build-and-push:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         
         - name: Build the Docker image
           run: docker build . --file Dockerfile --tag ghcr.io/${{ github.repository_owner }}/fish-microservice:latest

         - name: Log in to GitHub Container Registry
           run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

         - name: Push image to GitHub Container Registry
           run: docker push ghcr.io/${{ github.repository_owner }}/fish-microservice:latest
   ```

By using GHCR, we ensure that our project's container images are easily accessible, tightly integrated with our GitHub workflow, and free to distribute for our open-source project.
