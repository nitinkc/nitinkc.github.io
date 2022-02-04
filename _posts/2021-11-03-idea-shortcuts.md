---
# layout: static
title:  "IntelliJ Idea Shortcuts"
date:   2021-11-03 21:55:00
categories: Shortcuts
tags: [Shortcuts]
---

⌘Cmd ⇧Shift ^Ctrl ⌥Opt ⎋Esc ↵Return

⇧Shift ⎋Esc to hide a tool window


| Key | Details | 
| :---| :---    |      
|⌘E            |Move to the last location you edited.|

|⌘  + 1        |It activates the quick fix.|

## Coding Assistance

|**⇧ ⇧**       |Find All| 
|**⌘  ⇧ N**    |Search Resource|
|F2           |Goto Next coding Error|
|⌘ F1         |See Warning Errors, Press twice for details|
|**⌘ ⇧ F7**       |Highlighted All Usages|
|⇧⌘ F         |Find reference|
|Alt + F7     |Find a method where its used|
|⌘ J          |See documentation of a symbol at caret|
|⌘  +E        |Shows you a list of all open editors.|
|             |Use to move between open editors|
|⌘  + M       |Maximize or unmaximize your current tab.|
|⌘  + O       |Search a method within a  or|
|             |unmaximize your current tab.|
|⌘ + K/^ Sh K |Find instances fwd / backwards|
|**F3**           |Find uses in the same file|
|⌘  + B       |Build|
|⌘  +⇧+G      |Select an element and search its occurrences|
|⌘ ⇧ ⌫          |Jump back to previous edit|
|⌘[ /⌘]       |Move through navigation history|
|**⌘ ⌥ O**     |Optimize Imports|
|⌘  ⇧ O      ||
|**⌘  ⌥ L**  | Code Format - Selected Code and Entire File|
|⌘  ⌥  ⇧ L    |Reformatting Setting|
|⌘ P         |See Parameter Infor|
|⌘ ⇧ I        |See definition of a symbol at caret|


## Find & Replace in Files

|^Ctrl ⇧Shift F |Find in Files |
|W or ⌥Opt W    |Narrow search on Find While Searching|
| ^Ctrl ⇧Shift R   |Replace in Files |

## File Structure

|⌘Cmd  F12      |Display all methods in a file|
|⌘Cmd  7        |File Structure Tool Window|

## Declaration and Usage

|⌘Cmd B         |Jump to declaration of method, Toggle by clicking twice|
|⌥Opt F7        |Window for detailed view of usages  |

## Inheritance Hierarchy

|⌘Cmd ⌥Opt B        |See implementation of SomeInterface#foo|
|⌘Cmd U             |Navigate to super method|
|⌘Cmd  ⇧Shift H     |See Hierarchy Window|
|⌘Cmd H             |See Class Hierarchy|

## Recent Files and Locations

|⌘Cmd E             |Show recently opened Files|
|⌘Cmd ⇧Shift E             |See edited code is recently opened Files|


<!-- <table>
  <tr>
    <th>Key Combination</th>
    <th>Details</th>
  </tr>
{% for individual_shortcut in site.data.shortcuts %}
  <tr>
    <td> {{ individual_shortcut.keys }} </td>
    <td> {{ individual_shortcut.shortcut }} </td>
  </tr>
{% endfor %}

</table> -->

<!-- <ul>
{% for shortcut in site.data.shortcuts %}
  <li>
      {{ shortcut.keys }}
      {{ shortcut.shortcut }}
  </li>
{% endfor %}
</ul> -->