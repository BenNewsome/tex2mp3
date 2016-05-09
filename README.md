# tex2mp3
A .tex latex parser that can create plain text files and then convert them into mp3 files.

The program parses a standard .tex file and strips out all formatting information. Extra information is needed in the tex file for figures so that the text file can put a description of the image in place.

Extra information is added to the latex document with: 
%extra{ An image of a duck }

For example:

\begin{figure}
%extra{A figure of an example figure is shown here}
\centering
\includegraphics[width=5cm]{example_figure}
\caption{ This is a caption}
\label{example_figure}
\end{figure}


To ensure references to figures sound correct in the mp3 format, figures should be referenced in the following way:

\label{fig:A_Duck}

For example:

Rubber ducks are usialy yellow. A yellow duck can be seen in figure \cite{fig:A_duck}.

Will result in the text:

Rubber ducks are usually yellow. A yellow duck can be seen in figure, figure of A duck.



