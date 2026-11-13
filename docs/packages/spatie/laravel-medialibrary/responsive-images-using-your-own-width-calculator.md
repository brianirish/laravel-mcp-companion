# Spatie - Responsive Images/Using Your Own Width Calculator

Source: https://spatie.be/docs/laravel-medialibrary/v11/responsive-images/using-your-own-width-calculator

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Responsive-images

Using your own width calculator

Using your own width calculator
===============================

When generating images to be used in a `srcset`, the media library will calculate a set of target widths. The class responsible for generating the target widths can be specified in the `responsive_images.width_calculator` key of the `medialibrary` config file.

### ##The default calculator

The default width calculator shipped with the media library is named `FileSizeOptimizedWidthCalculator`. This class uses an algorithm which produces widths of which it is predicted that each one results in a file being ±70% of the filesize of the previous variation. The class will keep generating variations until the predicted file size is lower than 10 Kb or the target width is less than 20 pixels. So for an image with large dimensions the medialibrary will generate more variations than for an image with smaller dimensions.

### ##Using your own width calculator

In most cases the default `FileSizeOptimizedWidthCalculator` will generate pretty good results. But if for some reason you need to customize the behaviour you can specify your own class in the `responsive_images.width_calculator` of the `media-library` config file. A valid width calculator is any class that implements the `Spatie\MediaLibrary\ResponsiveImages\WidthCalculator\WidthCalculator` interface. Both the `calculateWidthsFromFile` and `calculateWidths` should return a `Collection` that contains the desired widths the responsive images should have.

Getting started with responsive images

Customizing the rendered HTML

Help us improve this page