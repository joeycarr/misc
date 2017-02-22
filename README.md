# Miscellaneous Tools

These are a bunch of tools that sit around in my bin. Most of them are
automation tools for some workflow that I cludged together.

## bitrate

    usage: bitrate [-h] movie_file

     Determines the video bitrate of a movie file.

      positional arguments:
         movie_file  The file to examine. Should be a file type supported by ffmpeg
      	             with a single video stream.

      optional arguments:
         -h, --help  show this help message and exit

## desty

    usage: desty [-h] [infile] [outfile]

    Remove styles from input HTML fragments leaving structural element intact.

    positional arguments:
      infile      Defaults to standard in.
      outfile     Defaults to standard out.

    optional arguments:
      -h, --help  show this help message and exit

## md5dir

    usage: md5dir [-h] [-s size] directory [...]
    
       -h    display this message
    
       -s    The minimum size of files to checksum; smaller files are
             ignored. Use the suffixes k, m, g, or t specify standard SI
             unit prefixes for 10^3, 10^6, 10^9, and 10^12
             respectively. The default suffix is k. The parameter must be
             an integer.
    
       directory  Specify one or more directories to check.

## pfft

    usage: pfft [-h] [--func func] infile outfile
    
    Runs a 2D Fast Fourier Transform (FFT) on the given input image. Depends
    on SciPy.
    
    positional arguments:
      infile       The image file to ingest.
      outfile      A writeable filename that can accept 16 bit output.
    
    optional arguments:
      -h, --help   show this help message and exit
      --func func  Which FFT function to call; can currently choose fft2 or fftn.

## shuffle

    usage: shuffle [-h] [infile] [outfile]
    
    Copies the lines from the input to output in a random order. Since this reads
    the entire input into memory, large files may be very slow.
    
    positional arguments:
      infile      The file containing the source text. Defaults to standard input.
                  Use '-' to signify standard input explicitly.
      outfile     The destination file to write random lines to. Defaults to
                  standard output. Use '-' to signify standard output explicitly.
    
    optional arguments:
      -h, --help  show this help message and exit

## tc

    usage: tc [-h] [-s] term [term ...]
    
    Add, subtract, or convert representations of time. As a convenience, you can
    separate the time fields with a dot (.) in lieu of the typical colon (:).
    
    positional arguments:
      term           A time represented in seconds, e.g. "90", or as hours,
                     minutes, and seconds, e.g. "1:20:37". By default, all terms
                     are summed. If you pass a negative sign, subsequent terms are
                     subtracted; if you pass a plus sign, subsequent terms are
                     again summed.
    
    optional arguments:
      -h, --help     show this help message and exit
      -s, --seconds  Display the result as a number of seconds rather than the
                     default HH:MM:SS.
    
## whead

    usage: whead [-h] [-n N] [infile [infile ...]]
    
    Display first words of a file
    
    positional arguments:
      infile
    
    optional arguments:
      -h, --help  show this help message and exit
      -n N
    
