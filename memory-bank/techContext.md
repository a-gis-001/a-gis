# Technical Context

## Core Technologies
1. Development
   - Python 3.x
   - pytest
   - black
   - mypy
   - pylint

2. AI/ML
   - Local LLMs
   - ChromaDB
   - LangChain
   - LlamaIndex
   - Ollama

3. Web
   - FastAPI
   - aiohttp
   - BeautifulSoup4
   - Selenium
   - Playwright

4. Data Processing
   - pandas
   - numpy
   - scipy
   - scikit-learn
   - transformers

## Infrastructure
1. Version Control
   - GITEA server
   - GitLab migration
   - Repository structure
   - Access control

2. AI Integration
   - Persona system
   - Learning framework
   - Contribution tracking
   - Usage analytics

3. Distribution
   - Code distillation
   - Hash-based functions
   - Version control
   - Dependency management

4. Testing
   - Coverage requirements
   - Automated verification
   - Integration testing
   - Performance testing

## Development Setup
1. Environment
   - Python virtual environment
   - Development tools
   - Testing framework
   - Documentation system

2. Tools
   - IDE configuration
   - Code formatting
   - Type checking
   - Linting
   - Testing

3. CI/CD
   - Automated testing
   - Coverage reporting
   - Documentation generation
   - Deployment pipeline

4. Monitoring
   - Performance tracking
   - Error logging
   - Usage analytics
   - Health checks

## Technical Constraints
1. Function Design
   - Keyword-only arguments
   - Type hints
   - Standardized returns
   - Input echoing
   - One function per file
   - Non-public functions
   - Internal imports

2. Testing
   - 100% coverage requirement
   - Automated verification
   - Integration testing
   - Performance testing
   - Edge case coverage

3. AI Integration
   - Local-first approach
   - Privacy preservation
   - Ethical considerations
   - Performance optimization
   - Resource management

4. Distribution
   - Code distillation
   - Hash generation
   - Version control
   - Dependency resolution
   - Security measures

5. Homepage
   - Real-time updates
   - Interactive elements
   - Performance optimization
   - Resource management
   - Security measures

6. App Platform
   - Hosting infrastructure
   - Version control
   - Security framework
   - Performance monitoring
   - Resource management

## Dependencies
1. Core
   - A_GIS.Code
   - A_GIS.Math
   - A_GIS.File
   - A_GIS.Text
   - A_GIS.Time

2. AI
   - A_GIS.Llm
   - A_GIS.Ai
   - A_GIS.Document
   - A_GIS.Image
   - A_GIS.Visual

3. Integration
   - A_GIS.Conversation
   - A_GIS.Data
   - A_GIS.Dev
   - A_GIS.Log
   - A_GIS.Cli

4. Testing
   - pytest
   - pytest-cov
   - pytest-asyncio
   - pytest-mock
   - pytest-xdist

5. Homepage
   - Image generation
   - Real-time updates
   - Interactive elements
   - Performance monitoring
   - Security framework

6. App Platform
   - Hosting system
   - Version control
   - Security framework
   - Performance monitoring
   - Resource management

## Image Comparison Dependencies

The image comparison functionality relies on several key libraries:

1. PIL (Python Imaging Library)
   - Used for image loading and basic operations
   - Supports multiple image modes (RGB, RGBA, Grayscale)

2. NumPy
   - Handles array operations for image data
   - Used for MSE calculations
   - Provides efficient array manipulation

3. scikit-image
   - Provides SSIM implementation
   - Handles structural similarity calculations
   - Supports different image modes and window sizes

### Technical Requirements

1. Image Size Requirements
   - Minimum size: 7x7 pixels for SSIM calculations
   - No maximum size limit
   - Must have same dimensions for comparison

2. Supported Image Modes
   - RGB (3 channels)
   - RGBA (4 channels)
   - Grayscale (1 channel)

3. Performance Considerations
   - SSIM calculations scale with image size
   - Large images may require significant memory
   - MSE calculations are more efficient 