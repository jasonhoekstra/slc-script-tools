<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:param name="AssessmentReportingMethod" select="'Number score'"/>
    <xsl:template match="/" xml:space="preserve">
<InterchangeStudentAssessment xmlns="http://ed-fi.org/0100"><xsl:for-each select="//row">
    <StudentAssessment>
        <AdministrationDate><xsl:value-of select="AdministrationDate"/></AdministrationDate>
        <RetestIndicator>Primary Administration</RetestIndicator>
        <ScoreResults AssessmentReportingMethod="{$AssessmentReportingMethod}">
          <Result><xsl:value-of select="ScoreResults_Results"/></Result> 
        </ScoreResults>        
        <GradeLevelWhenAssessed><xsl:value-of select="GradeLevelWhenAssessed"/></GradeLevelWhenAssessed>
        <StudentReference> 
           <StudentIdentity> 
                <StudentUniqueStateId><xsl:value-of select="StudentUniqueStateId"/></StudentUniqueStateId> 
           </StudentIdentity> 
        </StudentReference> 
        <AssessmentReference>
                <AssessmentIdentity> 
                <AssessmentTitle><xsl:value-of select="AssessmentIdentificationCode"/></AssessmentTitle>
				<AcademicSubject>Mathematics</AcademicSubject>
				<GradeLevelAssessed><xsl:value-of select="GradeLevelWhenAssessed"/></GradeLevelAssessed>
				<Version>1</Version> 
           </AssessmentIdentity>
        </AssessmentReference> 
    </StudentAssessment></xsl:for-each>
 </InterchangeStudentAssessment>
    </xsl:template>
</xsl:stylesheet>