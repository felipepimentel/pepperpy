import asyncio

from pepperpy.core import Application
from pepperpy.storage import StorageModule


async def main():
    # Configure storage module
    app = Application()

    storage = (
        StorageModule.create()
        .configure(
            base_path="data/storage",
            processors={
                "image": {"max_size": 1024, "formats": ["JPEG", "PNG"]},
                "pdf": {"compress": True, "extract_text": True},
            },
        )
        .build()
    )

    app.add_module(storage)

    async with app.run():
        # Save and process image
        image_info = await storage.save_file(
            "large_image.jpg", process=True, compress=True
        )
        print(f"Saved image: {image_info}")

        # Read and process PDF
        pdf_content = await storage.read_file("document.pdf", decompress=True)

        # List all image files
        images = await storage.list_files(pattern="*.{jpg,png,gif}", recursive=True)
        for image in images:
            print(f"Found image: {image.name} ({image.size} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
