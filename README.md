# ISR18

## Perf Board Wiring Diagram

![image](https://github.com/VT-HPS/ISR18/blob/main/Pictures/HPS%20Perfboard%20Wiring%20Diagram.png)

## Raspberry Pi 4B Pin Setup

![image](https://github.com/VT-HPS/ISR18/blob/cea95439157fb11f8bce3168e55f9beddc98750a/Pictures/Raspberry_Pi_Pins.png)
![image](https://github.com/VT-HPS/ISR18/blob/cea95439157fb11f8bce3168e55f9beddc98750a/Pictures/Raspberry_Pi_Pin_Specs.png)

## SSH-ing into Raspberry Pi in the HPS Bay

1. Your laptop’s wifi  =  Eduroam
2. RP’s wifi  =  Eduroam
3. Go into command prompt
    1. ssh hps@IP_ADDRESS
        1. If in the bay ip address might me 172.29.211.232
        2. ask for password from LE - hint: its 3 letters

## IMU

[IMU website](https://ozzmaker.com/product/berryimu-accelerometer-gyroscope-magnetometer-barometricaltitude-sensor/)

# Vim Cheatsheet

## Generally helpful stuff

    Open a file for editing             vim path/to/file
    Return to Normal mode               ESC   or <CTRL>+C
    Close a file without edits          :q
    Close a file saving edits           :wq
    Close a file ignoring edits         :q!

## Navigating around text
You have to be in Normal mode. Use ESC to get out of Visual, Replace, or Insert mode.

    (cursor left)                       h
    (cursor down)                       j
    (cursor up)                         k
    (cursor right)                      l
    next word                           e
    Jump to the first line              gg
    Jump to the last line               G

## Entering Text

    Insert text before cursor               i
    Insert text after cursor                a

## Working with multiple files

    Open a file in a horizontal split   :sp path/to/file.txt
    Open a file in a vertical split     :vsp path/to/file.txt
    Move to a split window page         <CTRL>+w and a direction key (h, j, k, or l)
    Move to next window pane            <CTRL>w w
    Make selected pane bigger           CTRL>w +  (yes, you need the shift key for the plus)
    Make selected pane smaller          <CTRL>w -
    
## Searching

    Search for a word                       /<word>
    Go to next match                        n
    Find and replace on line                :s/<find>/<replace>
    Find and replace globally               :%s/<find>/<replace>//gc


## Manipulating text
    
    cut the current line                dd
    copy the current line               yy
    paste below current line            p
    paste above current line            P
    Remove the character under cursor   x
    Remove the character before cursor  X
    Delete the word under cursor        de
    Delete to the end of the line       d$

    Remove five lines starting here     5dd
    Copy five lines starting here       5yy 

    indent this line                    >>
    indent five lines starting here     5>>

    Replace mode (overtype)             r

## Visual Advanced selection

    Visual mode                         v
    Visual Line mode                    V
    Visual Block mode                   <CTRL>v

## Working with NERDTree

    Open the NERDTree                   :NERDTree
    Toggle the NERDTree on and off      :NERDTreeToggle
    Open selected file                  <ENTER>
    Open selected file in horiz. split  i
    Open selected file in vert. split   v
    File menu                           m
    Help                                ?

## Commands:

    Run a command                           :!<command>
    Open a shell                            :sh

## Tasks

Combine Visual mode and cursor movement + Yank to copy or delete blocks

    Remove 5 lines                      Vjjjdd  (Visual Line mode, highlights line 1, jj to go Down two lines, dd to delete)

Create a custom Map Leader key to make it easy to run your own commands. We'll make it easy to show and hide NERDtree with a simple shortcut. Add these two lines to your .vimrc file:

    let mapleader = ","  
    map <Leader>d :NERDTreeToggle<CR> :set number<CR>   

With that, you can open and close NERDTree with

    ,d

in Normal mode.
