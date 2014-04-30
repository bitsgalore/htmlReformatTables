##About this software
Reformat tables in HTML document so that [Pandoc](http://johnmacfarlane.net/pandoc/)c will be able to convert them to
(almost) proper [Markdown Extra](http://michelf.ca/projects/php-markdown/extra/) tables. Written specifically for HTML that was exported
by MS Word. For each table, this script does the following:

1. Wrap first row in thead element and change td elements there to th
2. Wrap remaining rows in tbody elements
3. Remove outer p element from all table cells

Resulting html can be converted to Markdown with [Pandoc](http://johnmacfarlane.net/pandoc/), using the following command:

    pandoc -f html -t markdown_phpextra file.html > file.md
    
##Notes, hints, warnings

1. When you export your source document in MS Word, select *Web Page, Filtered*
2. Before using this script, clean up MS Word-generated HTML with [tidy](http://infohound.net/tidy/)
3. Table conversion isn't 100% fool-proof, and may not work for all documents!
4. Even if subsequent Markdown conversion with Pandoc is successful, you
   will probably need to do a fair bit of manual editing afterwards. 
5. Script was specifically written to help conversion of *one* single document, so don't expect this to be generic ("hope for the worst, expect hell") 
6.  Use at your own risk!
