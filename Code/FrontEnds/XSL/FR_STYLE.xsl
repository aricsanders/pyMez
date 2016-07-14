<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>

<xsl:template match="/">
  <html>
  <body>
  <h2>File Registry</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th align="left">Id</th>
        <th align="left">URL</th>
<th align="left">Type</th>

<th align="left">Date</th>

<th align="left">Host</th>

      </tr>
      <xsl:for-each select="File_Registry/File">
      <tr>
        <td><xsl:value-of select="@Id"/></td>
	

        <td><a><xsl:attribute name="href"> <xsl:value-of select="@URL" /> </xsl:attribute> 
<xsl:value-of select="@URL"/></a></td>
<td><xsl:value-of select="@Type"/></td>
<td><xsl:value-of select="@Date"/></td>
<td><xsl:value-of select="@Host"/></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>