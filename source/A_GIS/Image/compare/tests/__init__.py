"""Tests for A_GIS.Image.compare module.

This module contains comprehensive tests for the image comparison functionality,
including:
- Basic comparison tests (identical, similar, different images)
- Edge cases (empty images, single pixel images)
- Error cases (invalid inputs, different modes)
- Different image modes (RGB, RGBA, grayscale)
"""

import numpy
import PIL.Image
import pytest
import A_GIS.Image.new
import A_GIS.Image.compare
import os
import tempfile

def _create_test_image(size=(100, 100), mode='RGB', color=(255, 0, 0)):
    """Create a test image with specified properties.
    
    Args:
        size: Image dimensions (width, height)
        mode: Image mode (RGB, RGBA, L)
        color: RGB/RGBA color tuple or grayscale value
        
    Returns:
        PIL.Image.Image: Test image with a checkerboard pattern
    """
    img = A_GIS.Image.new(size=size, mode=mode)
    
    # Create a checkerboard pattern
    if mode == 'L':
        pattern = numpy.zeros(size, dtype=numpy.uint8)
        pattern[::20, ::20] = 255  # White squares every 20 pixels
        img = PIL.Image.fromarray(pattern)
    else:
        pattern = numpy.zeros((size[1], size[0], 3 if mode == 'RGB' else 4), dtype=numpy.uint8)
        pattern[::20, ::20] = [255, 0, 0] if mode == 'RGB' else [255, 0, 0, 255]  # Red squares
        pattern[10::20, 10::20] = [0, 255, 0] if mode == 'RGB' else [0, 255, 0, 255]  # Green squares
        img = PIL.Image.fromarray(pattern)
    
    return img

def _create_similar_image(image, noise_factor=0.1):
    """Create a slightly modified version of input image.
    
    Args:
        image: Input PIL.Image or numpy array
        noise_factor: Amount of noise to add (0-1)
        
    Returns:
        PIL.Image.Image: Modified image with noise in a small region
    """
    if isinstance(image, PIL.Image.Image):
        image = numpy.array(image)
    
    # Create a copy
    modified = image.copy()
    
    # Add noise to a small region in the center
    h, w = image.shape[:2]
    center_y = h // 2
    center_x = w // 2
    region_size = int(min(h, w) * 0.1)  # 10% of image size
    
    # Create noise
    noise = numpy.random.normal(0, noise_factor * 255, (region_size, region_size))
    if len(image.shape) == 3:
        noise = noise[:, :, numpy.newaxis]  # Add channel dimension
    
    # Add noise to the region
    y_start = center_y - region_size // 2
    x_start = center_x - region_size // 2
    modified[y_start:y_start+region_size, x_start:x_start+region_size] = numpy.clip(
        modified[y_start:y_start+region_size, x_start:x_start+region_size] + noise,
        0, 255
    ).astype(numpy.uint8)
    
    return PIL.Image.fromarray(modified)

def _create_different_image(image):
    """Create a significantly different version of input image.
    
    Args:
        image: Input PIL.Image or numpy array
        
    Returns:
        PIL.Image.Image: Different image
    """
    if isinstance(image, PIL.Image.Image):
        image = numpy.array(image)
    
    # Invert the image
    different = 255 - image
    return PIL.Image.fromarray(different)

def test_identical_images():
    """Test comparison of identical images.
    
    Verifies that identical images:
    - Have MSE of 0
    - Have SSIM of 1.0
    - Are marked as similar
    """
    img = _create_test_image()
    result = A_GIS.Image.compare(image1=img, image2=img)
    assert result.are_similar
    assert result.mse == 0
    assert result.ssim == 1.0

def test_similar_images():
    """Test comparison of slightly different images.
    
    Verifies that images with small differences:
    - Have low but non-zero MSE
    - Have high but not perfect SSIM
    - Are marked as similar if within tolerance
    """
    img1 = _create_test_image()
    img2 = _create_similar_image(img1, noise_factor=0.1)  # 10% noise
    result = A_GIS.Image.compare(image1=img1, image2=img2, tolerance=0.84)
    print(f"\nSSIM value: {result.ssim}")  # Debug print
    print(f"MSE value: {result.mse}")  # Debug print
    
    # Always save images for inspection
    test_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\nSaving test images to: {test_dir}")
    img1.save(os.path.join(test_dir, "test_original.png"))
    img2.save(os.path.join(test_dir, "test_modified.png"))
    print(f"Original image: {os.path.join(test_dir, 'test_original.png')}")
    print(f"Modified image: {os.path.join(test_dir, 'test_modified.png')}")
    
    # Run assertions
    assert result.are_similar
    assert 0 < result.mse < 100
    assert 0.9 < result.ssim < 1.0

def test_different_images():
    """Test comparison of significantly different images.
    
    Verifies that very different images:
    - Have high MSE
    - Have low SSIM
    - Are marked as not similar
    """
    img1 = _create_test_image()
    img2 = _create_different_image(img1)
    result = A_GIS.Image.compare(image1=img1, image2=img2)
    assert not result.are_similar
    assert result.mse > 100
    assert result.ssim < 0.9

def test_different_modes():
    """Test comparison of images with different modes.
    
    Verifies that attempting to compare images with different modes
    raises a ValueError.
    """
    img1 = _create_test_image(mode='RGB')
    img2 = _create_test_image(mode='RGBA')
    with pytest.raises(ValueError):
        A_GIS.Image.compare(image1=img1, image2=img2)

def test_different_sizes():
    """Test comparison of images with different sizes.
    
    Verifies that attempting to compare images with different dimensions
    raises a ValueError.
    """
    img1 = _create_test_image(size=(100, 100))
    img2 = _create_test_image(size=(200, 200))
    with pytest.raises(ValueError):
        A_GIS.Image.compare(image1=img1, image2=img2)

def test_invalid_tolerance():
    """Test comparison with invalid tolerance value.
    
    Verifies that attempting to use a tolerance value outside [0,1]
    raises a ValueError.
    """
    img1 = _create_test_image()
    img2 = _create_test_image()
    with pytest.raises(ValueError):
        A_GIS.Image.compare(image1=img1, image2=img2, tolerance=1.5)

def test_invalid_input_types():
    """Test comparison with invalid input types.
    
    Verifies that attempting to compare with non-image inputs
    raises a TypeError.
    """
    img1 = _create_test_image()
    with pytest.raises(TypeError):
        A_GIS.Image.compare(image1=img1, image2="not an image")

def test_empty_images():
    """Test comparison of empty images.
    
    Verifies that empty images (0x0) are handled correctly:
    - Have MSE of 0
    - Have SSIM of 1.0
    - Are marked as similar
    """
    img1 = _create_test_image(size=(0, 0))
    img2 = _create_test_image(size=(0, 0))
    result = A_GIS.Image.compare(image1=img1, image2=img2)
    assert result.are_similar
    assert result.mse == 0
    assert result.ssim == 1.0

def test_single_pixel_images():
    """Test comparison of single pixel images.
    
    Verifies that single pixel images are handled correctly:
    - Have MSE of 0 for identical pixels
    - Have SSIM of 1.0 for identical pixels
    - Are marked as similar for identical pixels
    """
    img1 = _create_test_image(size=(1, 1))
    img2 = _create_test_image(size=(1, 1))
    result = A_GIS.Image.compare(image1=img1, image2=img2)
    assert result.are_similar
    assert result.mse == 0
    assert result.ssim == 1.0

def test_rgba_images():
    """Test comparison of RGBA images.
    
    Verifies that RGBA images are handled correctly:
    - Alpha channel is considered in comparison
    - Have MSE of 0 for identical images
    - Have SSIM of 1.0 for identical images
    - Are marked as similar for identical images
    """
    img1 = _create_test_image(mode='RGBA', color=(255, 0, 0, 128))
    img2 = _create_test_image(mode='RGBA', color=(255, 0, 0, 128))
    result = A_GIS.Image.compare(image1=img1, image2=img2)
    assert result.are_similar
    assert result.mse == 0
    assert result.ssim == 1.0

def test_grayscale_images():
    """Test comparison of grayscale images.
    
    Verifies that grayscale images are handled correctly:
    - Have MSE of 0 for identical images
    - Have SSIM of 1.0 for identical images
    - Are marked as similar for identical images
    """
    img1 = _create_test_image(mode='L', color=128)
    img2 = _create_test_image(mode='L', color=128)
    result = A_GIS.Image.compare(image1=img1, image2=img2)
    assert result.are_similar
    assert result.mse == 0
    assert result.ssim == 1.0 