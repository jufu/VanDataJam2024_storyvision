from modules.description_enhancer import DescriptionEnhancer


def test_enhance_description():
    """
    Tests the DescriptionEnhancer's ability to generate an engaging description.
    """
    # Initialize the DescriptionEnhancer
    enhancer = DescriptionEnhancer()

    # Sample caption to enhance (can use actual captions from previous modules)
    caption = "a cartoon of two girls talking to each other"

    # Generate the enhanced description
    enhanced_description = enhancer.enhance_description(caption)

    # Print the enhanced description
    print("Enhanced Description:", enhanced_description)


# Run the test if this script is executed directly
if __name__ == "__main__":
    test_enhance_description()
