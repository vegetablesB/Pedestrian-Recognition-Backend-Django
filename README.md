# Pedestrian-Recognition-Backend-Django
Pedestrian-Recognition Backend based on Django.

This is the backend code for iOS app in [Frontend design](https://github.com/vegetablesB/Pedestrian-Recognition-iOS-APP).

This is a RESTful API including following functions.
- Create, Get, and Update users and tokens.
- Create, Get, and Update recognition and upload images to a recognition.
- Make prediction for the image.
- Update image from user, slef draw rectangle
- Filter recipe based on tags and ingredients.

## Build and run in the docker

```bash
# build
docker-compose build
# run
docker-compose up
# test
docker-compose run --rm app sh -c "python manage.py test"
```

## API schema
<img width="1175" alt="image" src="https://user-images.githubusercontent.com/44360183/213370265-ee3bcd73-c84e-4995-93cf-5228489faef9.png">


## License
[MIT © Richard McRichface.](../LICENSE)
