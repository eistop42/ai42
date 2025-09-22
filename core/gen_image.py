import uuid
from yandex_cloud_ml_sdk import YCloudML

def generate_image(message):
    sdk = YCloudML(
        folder_id="",
        auth="",
    )

    model = sdk.models.image_generation("yandex-art")
    # configuring model for all of future runs
    model = model.configure(width_ratio=1, height_ratio=1)

    # Sample 1: simple run
    operation = model.run_deferred(message)
    result = operation.wait()

    return result.image_bytes

    # filename = str(uuid.uuid4()) + '.jpg'
    # # сохраняем в файл
    # with open(filename, 'wb') as f:
    #     f.write(result.image_bytes)


if __name__ == "__main__":
    generate_image('незнайка на луне')