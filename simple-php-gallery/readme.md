# README

HotLinks - Like HotCakes, but you click on them...

## Getting Started

**links.csv** : ```"colorInside","colorOutside","iconColor","font-awesome-icon","hrefLink","cardHeader","cardContent"```

## WTF is it

Place hyperlinks in a csv, give them a name, type a description and specify the style using CSS colours and a [font-awesome](https://fontawesome.com/v4.7.0/cheatsheet/) icon name.

### Is it fast

No.

### Is it efficient

No.

### Is it fun

You need a new hobby.

### Is it useful

I used it. That's enough.

## Usage

Simply edit the *links.csv* file to add additional items.

HTML Colors are used to define the background colors for each card using a radial gradient, as well as the Icon Color.

Icon images are font-awesome icons, so are specified according to the font-awesome 4 icon classes *fa fa-name*.

> Originally it used a newer font awesome library but the CDN became an issue, so it fell back to FA-4.

Format:

``` text
"colorInside","colorOutside","iconColor","font-awesome-icon","hrefLink","cardHeader","cardContent"
```

Example:

``` text
"#85929E","#2E4053","white","fa fa-ban","#","Lorem Ipsum","Lorem ipsum dolor sit amet."
```

## Icon Availablity

This app uses a local copy of the Font Awesome library (not a CDN). Included is a Font Awesome Free Web package, which does not support all available font awesome icons (e.g. brands). Swap out the fa folder with your Font Awesome distribution to get access to your additional icons. Info on the current version is available in */fa/version.txt*

## Data Integrity

Enscapulating the item values in quotes **(")** within the csv source is a strict requirement.

If you need to include a quote character within a field, such as a text description, use a another quote character on the enclosed quotation in order to escape the character so that the system knows to recognise it as part of the content.

``` text
"#85929E","#2E4053","white","fa fa-info","#","Using Quotes","This displays the use of ""Quoted Text"""
```

Blank lines in the csv end up with blank cards. Avoid whitespace.

### Skipping Fields

Don't skip any fields. If you don't want to specify a parameter, include it as a blank string.

Browsers are pretty robust, so they'll handle most garbage included in the csv, but it will break the card.

Skipping a field will result in the next field value being used incorrectly, so your description may become the heading etc.

If you fail to properly close a field within the csv (by not including the *"* quotation characters), the field value will be considered until it finds the next closing character (typically within the next line of the csv). This will result in both the affected cards being broken.

### Icon Colors

To use the default *"iconColor"*, include the color parameter as a blank string:

``` text
"#85929E","#2E4053","","fa fa-ban","#","Lorem Ipsum","Lorem ipsum dolor sit amet."
```

Failure to do so will result in the incorrect string values being put into the page template, so it's likely that the current card and the following card will be broken.

Current default color is #212529, which is set in the css:

``` css
.gallery.cards-gallery a {
  color: #212529;
}
```

## BG Colors

One of the easiest ways to obtain reasonable colors is to utilise the [Color Charts](https://htmlcolorcodes.com/color-chart/) from the *HTML Color Codes* website.

Simply select a color chart/ Pallete and use a matching light and dark color with similar hue (e.g. the second row and third to last row within the same column).

## Code Injection

None of the csv data is sanitised, so obviously it's possible to inject code into the page using the csv data.

Example:

``` text
"#85929E","#2E4053","white","fa fa-ban","#","Lorem Ipsum","</p><script>console.log('Do Something')</script><p>"
```

Considering this whole thing gets stitched together server side and is designed to be nothing more than a very simple way to create a multi-link landing page, I'm not even sure this counts as a risk factor. If you let people edit the CSV through a Web UI though, you're for sure gonna gets some XSS happenings in there.

In any event, this notice is just here to let you know you shouldn't use csv data from untrusted sources or remote web locations, obviously. Rather use a database, like a normal person.

For now we leave it as is.

## Motivation

A no-nonsense, straight forward, dynamic link gallery that is simple enough for almost anyone to use in nearly any environment.

## Use case

If you have a bunch of bookmarks or web locations that you use regularly or want to create a landing page/ access portal type site for others, just stick the links into the csv file and let the magic happen. Looks a lot prettier than:

```html
<a href="http://link.one">Link one</a>
<a href="http://link.two">Link two</a>
<a href="http://link.three">Link two</a>
```

## Issues

It's not well tested and was built from scratch, so expect issues. It is currenly lacking in accessibility.

## Compatibility

This site does not make use of polyfills or any fancy backend functions to support outdated or incompatible browsers. The results from the app push out simple pages with HTML5/CSS/JS.

## Disclaimer

This product comes without warranty and will eat your homework.

## Unlicensed
