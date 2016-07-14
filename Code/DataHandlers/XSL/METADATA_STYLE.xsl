<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>

<xsl:template match="/">
  <html>
  <body>
  <h1 align='center'><i>Metadata</i></h1>
    <xsl:apply-templates/>
  </body>
  </html>
</xsl:template>



  <xsl:template match="Notes">
  Notes: <span style="color:#ff0000">
  <xsl:value-of select="."/></span>
  <br />
 </xsl:template>


<xsl:template match="File">
<xsl:for-each select=".">   
       <b><a><xsl:attribute name="href"> <xsl:value-of select="@URL" />
 </xsl:attribute><xsl:attribute name="title">  <xsl:value-of select="@URL" />
 </xsl:attribute>
        <xsl:value-of select="@URL"/></a> </b>  <br/>
    <i>Id:<xsl:value-of select="@Id"/></i> <br/>
<i>Host:<xsl:value-of select="@Host"/></i> <br/>
<table border='true'>
<tr>
<td><xsl:apply-templates select="System_Metadata"/></td>
<td><xsl:apply-templates select="File_Metadata"/></td>
<td><xsl:apply-templates select="Image_Metadata"/></td>
</tr>
</table>
<xsl:apply-templates select="Python_Docstring"/>
    <hr/>
 </xsl:for-each> 
</xsl:template>

<xsl:template match="System_Metadata">
   <table border='true' title='System Metadata'>  
<caption>System Metadata</caption> 
<xsl:for-each select="@*">
    <tr>
    <td>
    <b><xsl:value-of select="name()"/></b>
    </td>
    <td>
    <xsl:value-of select="."/>
    </td>
    </tr>
  </xsl:for-each>
</table>
<br />
</xsl:template>
<xsl:template match="File_Metadata">
   <table border='true' title='File Metadata'>
<caption>File Metadata</caption>  
<xsl:for-each select="*">
    <tr>
    <td>
    <b><xsl:value-of select="name()"/></b>
    </td>
    <td>
    <xsl:value-of select="."/>
    </td>
    </tr>
  </xsl:for-each>
</table>
<br />
</xsl:template>
<xsl:template match="Image_Metadata">
   <table border='true' title='File Metadata'>  
<caption>Image Metadata</caption> 
<xsl:for-each select="*">
    <tr>
    <td>
    <b><xsl:value-of select="name()"/></b>
    </td>
    <td>
    <xsl:value-of select="."/>
    </td>
    </tr>
  </xsl:for-each>
</table>
<br />
</xsl:template>

<xsl:template match="Python_Docstring">

<xsl:for-each select=".">

    <b><xsl:value-of select="name()"/>: </b>
 
    <i><xsl:value-of select="."/></i> <br/>

  </xsl:for-each>

<br />
</xsl:template>
</xsl:stylesheet>