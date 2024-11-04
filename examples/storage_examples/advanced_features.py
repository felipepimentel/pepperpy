import asyncio

from pepperpy.core import Application
from pepperpy.storage import StorageModule
from pepperpy.storage.transforms import ImageTransform, TransformationPipeline


async def main():
    # Configure storage module
    app = Application()

    storage = (
        StorageModule.create()
        .configure(
            base_path="data/storage",
            processors={
                "image": {
                    "max_size": 1024,
                    "quality": 85,
                    "formats": ["JPEG", "PNG", "WEBP"],
                },
                "pdf": {"compress": True, "extract_images": True},
            },
            index_content=True,  # Enable content indexing
        )
        .build()
    )

    app.add_module(storage)

    async with app.run():
        # Process image with transformations
        pipeline = TransformationPipeline()
        pipeline.add_transform(
            ImageTransform(), max_size=800, format="WEBP", quality=85
        )

        # Save transformed image
        image_info = await storage.save_file(
            "original.jpg", "processed/image.webp", transform_pipeline=pipeline
        )
        print(f"Processed image: {image_info}")

        # Create PDF archive
        files = ["doc1.pdf", "doc2.pdf"]
        archive = await storage.operations.create_archive(
            files, "archives/documents.zip"
        )
        print(f"Created archive: {archive}")

        # Search content
        results = await storage.metadata.search("important document", field="content")
        for result in results:
            print(f"Found: {result['path']}")

        # Stream large file
        async for chunk in storage.operations.stream_file("large_video.mp4"):
            # Process chunk
            pass


if __name__ == "__main__":
    asyncio.run(main())
