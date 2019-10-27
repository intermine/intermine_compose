echo "Attempting docker login"
docker login -u "$DOCKER_REGISTRY_USER" -p "$DOCKER_REGISTRY_PASSWORD"
echo "Staring docker build"
docker build
      --tag "intermine/compose:latest"
      --tag "intermine/compose:$TRAVIS_COMMIT" .
echo "Pushing built image to the registry "
docker push "intermine/compose:latest"
docker push "intermine/compose:$TRAVIS_COMMIT"