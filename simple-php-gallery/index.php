<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="gallery" content="">
  <meta name="author" content="">
  <link rel='shortcut icon' type='image/x-icon' href='favicon.ico' />

  <title>Gallery</title>

  <link href="css.css" rel="stylesheet">
  <link href="card-scrollbar.css" rel="stylesheet">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
  <link href='http://fonts.googleapis.com/css?family=Noto+Sans:400,300,700' rel='stylesheet' type='text/css'>
</head>

<body>
  <section class="gallery cards-gallery">
    <div class="container">
      <div class="gallery-heading">
        <h2>Gallery</h2>
      </div>
      <div class="gallery-readme">
        <p>This gallery is a simple HTML template for creating a pretty list of items, information and links with CSS "cards".
        <br>You could use it on a storefront, landing page, dashboard or wherever you like.
        <br>It uses the bootstrap 4 CSS framework for responsive design and the Font Awesome 4 icons for inclusion of element symbols.
        <br>An html version of the page is availble in the <a href="https://github.com/zacharlie/zacharlie.github.io/simple-html-gallery">zacharlie.github.io</a> repo.</p>
      </div>
      <div class="row">

<?php

// current page number
$page = $_GET['page'];

$page = intval($page);

// if not defined set to zero
if ((empty($page)) == TRUE) {
    $page=0;
}

// if not valid integer set to zero
if (is_int($page) == FALSE) {
    $page=0;
}

// page numbers start at 1
if (($page<=0) == TRUE) {
    $page=1;
}

// maximum results per page
$limit = 12;

$counter = 0;

// count total lines (items) in csv
if (($handle = fopen('links.csv', 'r')) !== FALSE) {
    while (($data = fgetcsv($handle, 1)) !== FALSE) {
        $counter++;
    }
    $total = $counter;
    $counter = 0;
}

// Check for maximum possible pages
$pageMax = ceil($total / $limit);

if (($page > $pageMax) == TRUE) {
    $page = $pageMax;
}

$pagePrevious = $page - 1;
$pageNext = $page + 1;

$countCurrent = $page * $limit;
$countPrevious = $pagePrevious * $limit;

// load the link data from csv into cards
if (($handle = fopen('links.csv', 'r')) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ',', '"')) !== FALSE) {
        if (($counter >= $countPrevious && $counter < $countCurrent) !== FALSE) {
            echo '        <div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">';
            echo '          <div class="card border-0 cards-gallery-hover">';
            echo '            <a class="card-img-link" href="' . $data[4] . '">';
            echo '              <div style="background-image: radial-gradient(' . $data[0] . ',' . $data[1] . ')" alt="Card Image" class="card-img-top">';
            echo '                <div class="icon-flex-box" style="color: ' . $data[2] . '"><i class="' . $data[3] . '"></i></div>';
            echo '              </div>';
            echo '            </a>';
            echo '            <div class="card-body card-scrollbar">';
            echo '              <h6><a href="' . $data[4] . '">' . $data[5] . '</a></h6>';
            echo '              <p class="text-muted card-text">' . $data[6] . '</p>';
            echo '            </div>';
            echo '          </div>';
            echo '        </div>';
            echo "\n";
        }
        $counter++;
    }
    fclose($handle);
}

echo '      </div>' . "\n";

// Pagination Navbar

// extra page items for pagination
$pageMinus2 = $page - 2;
$pageMinus3 = $page - 3;
$pageMinus4 = $page - 4;
$pageMinus5 = $page - 5;
$pageMinus6 = $page - 6;
$pagePlus2 = $page + 2;
$pagePlus3 = $page + 3;
$pagePlus4 = $page + 4;
$pagePlus5 = $page + 5;
$pagePlus6 = $page + 6;

echo '      <div>' . "\n";
echo '        <nav aria-label="Gallery Navigation">' . "\n";
echo '          <ul class="pagination justify-content-center">' . "\n";
echo '            <li class="page-item">' . "\n";
if ($page==1) {
    echo '              <a class="page-link btn disabled" tabindex="-1" role="button" aria-disabled="true" href="?page=' . $pagePrevious . '">' . "\n";
    echo '                <span aria-hidden="true">&laquo;</span>' . "\n";
    echo '                <span class="sr-only">Previous</span>' . "\n";
    echo '              </a>' . "\n";
} else {
    echo '              <a class="page-link" href="?page=' . $pagePrevious . '" aria-label="Previous">' . "\n";
    echo '                <span aria-hidden="true">&laquo;</span>' . "\n";
    echo '                <span class="sr-only">Previous</span>' . "\n";
    echo '              </a>' . "\n";
}
echo '            </li>' . "\n";

// page links

// compensate for shortfall on high numbers
if ($pageMinus6 <= 1 ) {
} else if ($pageNext > $pageMax) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pageMinus6 . '">' . $pageMinus6 . '</a></li>' . "\n";
}
if ($pageMinus5 <= 1 ) {
} else if ($pagePlus2 > $pageMax) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pageMinus5 . '">' . $pageMinus5 . '</a></li>' . "\n";
}
if ($pageMinus4 <= 1 ) {
} else if ($pagePlus3 > $pageMax) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pageMinus4 . '">' . $pageMinus4 . '</a></li>' . "\n";
}

// previous pages
if ($pageMinus3 > 0) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pageMinus3 . '">' . $pageMinus3 . '</a></li>' . "\n";
}
if ($pageMinus2 > 0) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pageMinus2 . '">' . $pageMinus2 . '</a></li>' . "\n";
}
if ($pagePrevious > 0) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pagePrevious . '">' . $pagePrevious . '</a></li>' . "\n";
}

// current page
echo '            <li class="page-item active" role="button"><a class="page-link" href="?page='. $page . '">' . $page . '</a></li>' . "\n";

// next pages
if ($pageNext <= $pageMax) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pageNext . '">' . $pageNext . '</a></li>' . "\n";
}
if ($pagePlus2 <= $pageMax) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pagePlus2 . '">' . $pagePlus2 . '</a></li>' . "\n";
}
if ($pagePlus3 <= $pageMax) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pagePlus3 . '">' . $pagePlus3 . '</a></li>' . "\n";
}

// compensate for shortfall on low numbers
if ($pagePlus4 >= $pageMax) {
} else if ($pageMinus3 <= 0) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pagePlus4 . '">' . $pagePlus4 . '</a></li>' . "\n";
}
if ($pagePlus5 >= $pageMax) {
} else if ($pageMinus2 <= 0) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pagePlus5 . '">' . $pagePlus5 . '</a></li>' . "\n";
}
if ($pagePlus6 >= $pageMax) {
} else if ($pagePrevious <= 0) {
    echo '            <li class="page-item"><a class="page-link" href="?page=' . $pagePlus6 . '">' . $pagePlus6 . '</a></li>' . "\n";
}

echo '            <li class="page-item">' . "\n";
if ($pageNext > $pageMax) {
    echo '              <a class="page-link btn disabled" tabindex="-1" role="button" aria-disabled="true" href="?page=' . $pageNext . '">' . "\n";
    echo '                <span aria-hidden="true">&raquo;</span>' . "\n";
    echo '                <span class="sr-only">Next</span>' . "\n";
} else {
    echo '              <a class="page-link" href="?page=' . $pageNext . '" aria-label="Next">' . "\n";
    echo '                <span aria-hidden="true">&raquo;</span>' . "\n";
    echo '                <span class="sr-only">Next</span>' . "\n";
}
echo '              </a>' . "\n";
echo '            </li>' . "\n";
echo '          </ul>' . "\n";
echo '        </nav>' . "\n";
echo '      </div>' . "\n";

?>
    </div>
  </section>
</body>
</html>