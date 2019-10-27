docker login -u "$DOCKER_REGISTRY_USER" -p "$DOCKER_REGISTRY_PASSWORD"
docker build
      --tag "intermine/compose:latest"
      --tag "intermine/compose:$TRAVIS_COMMIT" .
docker push "intermine/compose:latest"
docker push "intermine/compose:$TRAVIS_COMMIT" .