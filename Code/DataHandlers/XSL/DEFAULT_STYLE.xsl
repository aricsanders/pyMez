<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<xsl:template match="*">
<html>
  <body>
    <table border='true' title='Element' style="background-color:gray;color:blue;text-align:center">    
        <tr>
            <tr title='Element'><td colspan='2'><h2 style='text-align:center;color:red;background-color:black'>
    <i> <span style='color=#B0B0B0 '> <xsl:for-each select="ancestor::*">
   <xsl:value-of select="name()"/>
 
   <xsl:if test="position() != last()">
   <xsl:text></xsl:text>
   </xsl:if>:
  </xsl:for-each></span><xsl:value-of select="name()"/></i></h2></td></tr>
    <td>
    <table border='true' title='Attributes' style="background-color:silver;color:blue;text-align:center;align:right">  
    <tr><td colspan='2'><span style='text-align:center'>
    <i><xsl:value-of select="name()"/> Attributes</i></span></td>
    </tr>
    <xsl:for-each select="@*">
    <tr>
    <td>
    <b><xsl:value-of select="name()"/></b>
    </td>
    <td style='background-color:white;'>
    <xsl:value-of select="."/>
    </td>
   </tr>
    </xsl:for-each>
    </table>
</td>
 <tr title='Element Text' ><td colspan='2' style='background-color:white;'><xsl:value-of select="text()"/></td></tr> </tr>

</table>
<br/><br/>
<hr/>
 
<xsl:apply-templates select='*'/> 


  </body>
  </html>
</xsl:template>


</xsl:stylesheet>