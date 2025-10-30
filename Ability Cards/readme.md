# Ability cards for Shadows of Brimstone

MiniUSA cards for the main heroes upgrades

# Files

../Fonts/UsedFonts => install them both in the machine and in the WSL (copy to /usr/share/fonts/(new folder) and run sudo fc-cache -fv)

cards.csv = a semicolon separated value table with the data. (UTF-8) 
    One line per card.
    The Header matches with the %FIELD% of the SVG template
    To open in excel mind to use UTF-8 as encoding. Save as CVS With UTF-8 Encoding!!!

template.svg = the card template
    The card base to generate.
    The texts are going to be filled to %FIELD%, matching with the header on cards.txt.
    Some cards need two lines for the title (name). They use %NAME2% placeholder, not %NAME%
    
Para imprimir:

    make generatesvg
    make generatepng
    make generatepdf

    Open PDF in Chrome
    Click <CTLR-P>
    Click on More Settings
    Mark Two Sided
    Choose Flip on Short Edge
    Mark Scale Custom
    Choose 100 
