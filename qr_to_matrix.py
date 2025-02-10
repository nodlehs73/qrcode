from PIL import Image
import random, string
import secrets
def png_to_binary_matrix(file_path):
    """
     Face conversia din o poza cu qr cod in matrice de 0 si 1 unde 1 inseamna negru si 0 inseamna alb
    :param file_path:
    :return:
    """
    img = Image.open(file_path).convert("L")  # 'L' mode is for grayscale

    width, height = img.size
    if width != height:
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        img = img.crop((left, top, right, bottom))

    width, height = img.size
    assert (width // 10 - 17) % 4 == 0
    version = (width // 10 - 17) // 4

    target_size = width // 10

    img_resized = img.resize((target_size, target_size), Image.NEAREST)


    # Step 3: Convert to binary (1 = black, 0 = white) using threshold
    # Here, we use a lambda function to apply the threshold
    binary_img = img_resized.point(lambda x: 1 if x < 128 else 0, mode='1')

    # Step 4: Convert the binary image to a binary matrix (list of lists)
    binary_matrix = []
    for y in range(target_size):
        row = []
        for x in range(target_size):
            pixel = binary_img.getpixel((x, y))
            row.append(pixel)
        binary_matrix.append(row)

    return binary_matrix, version


# Path to your QR code PNG file


def matrix_to_qrcode(matrix, scale, output_file, structured_append):
    if not matrix:
        raise ValueError("The matrix is empty.")

    height = len(matrix)
    width = len(matrix[0])

    print (width, height)
    # Create a new image with white background
    img = Image.new('RGB', (width * scale, height * scale), 'white')
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            color = (0, 0, 0) if matrix[y][x] == 1 else (255, 255, 255)
            for i in range(scale):
                for j in range(scale):
                    pixels[x * scale + i, y * scale + j] = color

    if structured_append == True:
        file_name = "".join (secrets.choice (string.ascii_uppercase) for _ in range (8)) + ".png"
        print(f"QR code image saved as {"photos/" + file_name}")
        img.save("photos/" + file_name)
    else:
        print(f"QR code image saved as {output_file}")
        img.save (output_file)


# Example us

# matrix_to_qrcode(binary_matrix, scale=20, output_file='qrcode.png')
