Checking updates (run 'admtooCreateHtml -f' to force generation)...
'users' updated
Creating HTML files into /home/laogtool/laogtool/Production/data/www/default
Store xml db file revision '$Revision: 1.3242 $' into revision.txt
Generate directory/directory.csv
CMD:  xsltproc --path .:../config:/home/laogtool/laogtool/Production/DEVELOPMENT/config:/home/laogtool/laogtool/Production/data/db/default/ -o directory.csv admtooXmlToDirectory.xsl /home/laogtool/laogtool/Production/data/db/default/admtooDatabase.xml
                                                                [  OK  ]
Push it onto the webserver
CMD:  curl -F userfile=@directory.csv http://ipag.osug.fr/annuaire_ipag/push.php
<pre> DEBUG: file uploaded successfully by web server </pre>
<pre> DEBUG: import OK into annuairetest </pre>
<pre> DEBUG: import OK into annuaire </pre>
                                             
[ fichiers de données pour l'annuaire et le kifekoi ]

Creating twiki file: Ipag/Intranet/InfoDocMailAliases.txt
Creating twiki file: Ipag/Intranet/KifekoiTable.txt


[ génération des groupes twiki - done ]

Creating twiki file: Main/IpagIpagsiteGroup.txt
Creating twiki file: Main/IpagPermGroup.txt
Creating twiki file: Main/IpagAdminGroup.txt
Creating twiki file: Main/IpagChercheurGroup.txt
Creating twiki file: Main/IpagChercheuraffilieGroup.txt
Creating twiki file: Main/IpagIngetechGroup.txt
Creating twiki file: Main/IpagThesardGroup.txt
Creating twiki file: Main/IpagInvitesGroup.txt
Creating twiki file: Main/IpagPostdocGroup.txt
Creating twiki file: Main/IpagStageGroup.txt
Creating twiki file: Main/IpagMaster2Group.txt
Creating twiki file: Main/IpagAstromolGroup.txt
Creating twiki file: Main/IpagCristalGroup.txt
Creating twiki file: Main/IpagFostGroup.txt
Creating twiki file: Main/IpagPlanetoGroup.txt
Creating twiki file: Main/IpagSherpasGroup.txt
Creating twiki file: Main/IpagOdysseyGroup.txt
Creating twiki file: Main/IpagExoplanetesGroup.txt
Creating twiki file: Main/IpagServicesGroup.txt
Creating twiki file: Main/IpagSafirGroup.txt
Creating twiki file: Main/IpagDmz98Group.txt
Creating twiki file: Main/IpagGuepardGroup.txt
Creating twiki file: Main/IpagPicsouGroup.txt
Creating twiki file: Main/IpagMauiGroup.txt
Creating twiki file: Main/IpagExtra-blueGroup.txt
Creating twiki file: Main/IpagVirtisGroup.txt
Creating twiki file: Main/IpagSphereGroup.txt
Creating twiki file: Main/IpagGravityGroup.txt
Creating twiki file: Main/IpagPionierGroup.txt
Creating twiki file: Main/IpagElectroniqueGroup.txt
Creating twiki file: Main/IpagExtraGroup.txt
Creating twiki file: Main/IpagDirectionGroup.txt
Creating twiki file: Main/IpagConsertGroup.txt
Creating twiki file: Main/IpagJmmcGroup.txt
Creating twiki file: Main/IpagNeatGroup.txt
Creating twiki file: Main/IpagInformatiqueGroup.txt
Creating twiki file: Main/IpagRadarGroup.txt
Creating twiki file: Main/IpagMarsisGroup.txt
Creating twiki file: Main/IpagSharadGroup.txt
Creating twiki file: Main/IpagSpectroGroup.txt
Creating twiki file: Main/IpagAeroGroup.txt
Creating twiki file: Main/IpagAmberGroup.txt
Creating twiki file: Main/IpagXlabuserGroup.txt
Creating twiki file: Main/IpagWeb-exochemistryGroup.txt
Creating twiki file: Main/IpagWeb-hydridesGroup.txt
Creating twiki file: Main/IpagWeb-stflorentGroup.txt
Creating twiki file: Main/IpagWeb-focusGroup.txt
Creating twiki file: Main/IpagWeb-chemical-cosmosGroup.txt
Creating twiki file: Main/IpagWeb-rt13Group.txt
Creating twiki file: Main/IpagWeb-asaGroup.txt
Creating twiki file: Main/IpagWeb-nika2Group.txt
Creating twiki file: Main/IpagWeb-descGroup.txt
Creating twiki file: Main/IpagWeb-benchmarksGroup.txt
Creating twiki file: Main/IpagNitrogenGroup.txt


Creating twiki file: Ipag/Intranet/InfoDocMailingListDiagram.txt


Creating xhtml file: mailingLists/site.ipag.html
Creating xhtml file: mailingLists/ipag.html
Creating xhtml file: mailingLists/permanent.ipag.html
Creating xhtml file: mailingLists/it.ipag.html
Creating xhtml file: mailingLists/administratif.ipag.html
Creating xhtml file: mailingLists/ingetech.ipag.html
Creating xhtml file: mailingLists/chercheur.ipag.html
Creating xhtml file: mailingLists/chercheuraffilie.ipag.html
Creating xhtml file: mailingLists/thesard.ipag.html
Creating xhtml file: mailingLists/postdoc.ipag.html
Creating xhtml file: mailingLists/invite.ipag.html
Creating xhtml file: mailingLists/master.ipag.html
Creating xhtml file: mailingLists/stagiaire.ipag.html
Creating xhtml file: mailingLists/conseil-labo.ipag.html
Creating xhtml file: mailingLists/astromol.ipag.html
Creating xhtml file: mailingLists/fost.ipag.html
Creating xhtml file: mailingLists/cristal.ipag.html
Creating xhtml file: mailingLists/planeto.ipag.html
Creating xhtml file: mailingLists/sherpa.ipag.html
Creating xhtml file: mailingLists/odyssey.ipag.html
Creating xhtml file: mailingLists/support-batiment.ipag.html
Creating xhtml file: mailingLists/support-batimentd.ipag.html
Creating xhtml file: mailingLists/support-info.ipag.html
Creating xhtml file: mailingLists/chs.ipag.html
Creating xhtml file: mailingLists/comelec.ipag.html
Creating xhtml file: mailingLists/ccmgr.ipag.html
Creating xhtml file: mailingLists/docmgr.ipag.html
Creating xhtml file: mailingLists/campi.ipag.html
Creating xhtml file: mailingLists/publi.ipag.html
Creating xhtml file: mailingLists/cell-com.ipag.html
Creating xhtml file: mailingLists/webmaster.ipag.html
Creating xhtml file: mailingLists/caq.ipag.html
Creating xhtml file: mailingLists/gestion.ipag.html
Creating xhtml file: mailingLists/comite-theses.ipag.html
Creating xhtml file: mailingLists/secretariat.ipag.html
Creating xhtml file: mailingLists/formation.ipag.html
Creating xhtml file: mailingLists/resp-seminaire.ipag.html
Creating xhtml file: mailingLists/direction.ipag.html
                                                                [  OK  ]

[ copie des fichiers générés précédemment - done ]


Update htgroup files
CMD:  ssh laogtool@ipag.obs.ujf-grenoble.fr admtooGenerateHtgroupsFromTWikiGroups
Searching twiki group file from /var/www/twiki/data/Main/
 - analysing /var/www/twiki/data/Main/IpagWeb-hydridesGroup.txt
 - analysing /var/www/twiki/data/Main/LaogInvitesGroup.txt
 - analysing /var/www/twiki/data/Main/LaogPostdocGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSpectro-g1Group.txt
 - analysing /var/www/twiki/data/Main/ProjetFocusGroup.txt
 - analysing /var/www/twiki/data/Main/LaogAmberGroup.txt
 - analysing /var/www/twiki/data/Main/IpagInformatiqueGroup.txt
 - analysing /var/www/twiki/data/Main/IpagDirectionGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetTholinsGroup.txt
 - analysing /var/www/twiki/data/Main/LaogElectroniqueGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-nika2Group.txt
 - analysing /var/www/twiki/data/Main/IpagAero-l1Group.txt
 - analysing /var/www/twiki/data/Main/IpagTheseImageReconstructionGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCristalGroup.txt
 - analysing /var/www/twiki/data/Main/IpagMarsisGroup.txt
 - analysing /var/www/twiki/data/Main/IpagMaster2Group.txt
 - analysing /var/www/twiki/data/Main/IpagAeroGroup.txt
 - analysing /var/www/twiki/data/Main/IpagInvitesGroup.txt
 - analysing /var/www/twiki/data/Main/IpagSafirGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSpectro-g2Group.txt
 - analysing /var/www/twiki/data/Main/LaogRadar-l1Group.txt
 - analysing /var/www/twiki/data/Main/LaogInstrumentationGroup.txt
 - analysing /var/www/twiki/data/Main/LaogColloqueInsuRD2011Group.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationCafeAstroGroup.txt
 - analysing /var/www/twiki/data/Main/LaogJmmcGroup.txt
 - analysing /var/www/twiki/data/Main/LaogStageGroup.txt
 - analysing /var/www/twiki/data/Main/LaogPermanentsGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationZCMaGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetMuseGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-exochemistryGroup.txt
 - analysing /var/www/twiki/data/Main/IpagHygieneSecuriteGroup.txt
 - analysing /var/www/twiki/data/Main/IpagNitrogenGroup.txt
 - analysing /var/www/twiki/data/Main/IpagSharadGroup.txt
 - analysing /var/www/twiki/data/Main/LaogMaster2Group.txt
 - analysing /var/www/twiki/data/Main/IpagGroupeTechniqueManagementGroup.txt
 - analysing /var/www/twiki/data/Main/IpagFostGroup.txt
 - analysing /var/www/twiki/data/Main/LaogPermGroup.txt
 - analysing /var/www/twiki/data/Main/LaogChercheurGroup.txt
 - analysing /var/www/twiki/data/Main/IpagAero-l2Group.txt
 - analysing /var/www/twiki/data/Main/ProjetOrbispaceGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatEsaSmallMissionGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetFfreeSystemeGroup.txt
 - analysing /var/www/twiki/data/Main/IpagThesardGroup.txt
 - analysing /var/www/twiki/data/Main/IpagRecrutementsGroup.txt
 - analysing /var/www/twiki/data/Main/IpagAQGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-focusGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-benchmarksGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationANRSmartLasirGroup.txt
 - analysing /var/www/twiki/data/Main/LaogXlabuserGroup.txt
 - analysing /var/www/twiki/data/Main/IpagPionierGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSharadGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationTheiaGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationCstblGroup.txt
 - analysing /var/www/twiki/data/Main/LaogGrilDirectionGroup.txt
 - analysing /var/www/twiki/data/Main/LaogInformatiqueGroup.txt
 - analysing /var/www/twiki/data/Main/LaogLaogsiteGroup.txt
 - analysing /var/www/twiki/data/Main/LaogAdministrationGroup.txt
 - analysing /var/www/twiki/data/Main/TWikiAdminGroup.txt
 - analysing /var/www/twiki/data/Main/IpagPicsouGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSherpasGroup.txt
 - analysing /var/www/twiki/data/Main/Projet2GFTGroup.txt
 - analysing /var/www/twiki/data/Main/LaogThesardGroup.txt
 - analysing /var/www/twiki/data/Main/IpagVirtisGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationExoPlanetesGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-chemical-cosmosGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetGravityGroup.txt
 - analysing /var/www/twiki/data/Main/LaogLaogGroup.txt
 - analysing /var/www/twiki/data/Main/IpagIntranetGroup.txt
 - analysing /var/www/twiki/data/Main/IpagAstromolGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetTotemsGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetDarwinGroup.txt
 - analysing /var/www/twiki/data/Main/IpagRadarGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSpectro-g3Group.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatCosmicVision2Group.txt
 - analysing /var/www/twiki/data/Main/ProjetConsertOperationsGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetVsiGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationImgAOGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationASAGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetAssertGroup.txt
 - analysing /var/www/twiki/data/Main/IpagMauiGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetExtraGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetOrbiTreatGroup.txt
 - analysing /var/www/twiki/data/Main/IpagJmmcGroup.txt
 - analysing /var/www/twiki/data/Main/IpagDmz98Group.txt
 - analysing /var/www/twiki/data/Main/ProjetEELTCAMGroup.txt
 - analysing /var/www/twiki/data/Main/LaogMecaniqueGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationHD45677Group.txt
 - analysing /var/www/twiki/data/Main/IpagCommunicationGroup.txt
 - analysing /var/www/twiki/data/Main/LaogAdminGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationVdiOsugAGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCdGroup.txt
 - analysing /var/www/twiki/data/Main/FloralisGroup.txt
 - analysing /var/www/twiki/data/Main/LpgPermanentsGroup.txt
 - analysing /var/www/twiki/data/Main/NobodyGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationNeatDemoGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetSwiftsGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetRapidGroup.txt
 - analysing /var/www/twiki/data/Main/JmmcCSGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationStagesM2Group.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationPFIGroup.txt
 - analysing /var/www/twiki/data/Main/IpagIngetechGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatEsaM3MissionGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationHPerGroup.txt
 - analysing /var/www/twiki/data/Main/IpagGravityGroup.txt
 - analysing /var/www/twiki/data/Main/IpagAstrochimieGroup.txt
 - analysing /var/www/twiki/data/Main/IpagStageGroup.txt
 - analysing /var/www/twiki/data/Main/IpagPostdocGroup.txt
 - analysing /var/www/twiki/data/Main/IpagChercheurGroup.txt
 - analysing /var/www/twiki/data/Main/IpagIntranetAdminGroup.txt
 - analysing /var/www/twiki/data/Main/IpagAdminGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetFocusDirectionGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationAmberHAeBesGroup.txt
 - analysing /var/www/twiki/data/Main/IpagAmberGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetFocusBureauGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatMicroNeatGroup.txt
 - analysing /var/www/twiki/data/Main/IpagConsertGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSoftGroup.txt
 - analysing /var/www/twiki/data/Main/LaogAero-l2Group.txt
 - analysing /var/www/twiki/data/Main/IpagPermGroup.txt
 - analysing /var/www/twiki/data/Main/IpagGroupeTechniqueDirectionGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationHS3FGroup.txt
 - analysing /var/www/twiki/data/Main/JmmcNotifyGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetPionierSystemeGroup.txt
 - analysing /var/www/twiki/data/Main/IpagOdysseyGroup.txt
 - analysing /var/www/twiki/data/Main/IpagClGroup.txt
 - analysing /var/www/twiki/data/Main/IpagNeatGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-rt13Group.txt
 - analysing /var/www/twiki/data/Main/IpagSpectro-g1Group.txt
 - analysing /var/www/twiki/data/Main/LaogGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationCSTGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetWisdomGroup.txt
 - analysing /var/www/twiki/data/Main/LaogGrilGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNaosGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatPhaseZeroGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetConsertSimulationGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetFocusConseilGroup.txt
 - analysing /var/www/twiki/data/Main/LaogRdeGroup.txt
 - analysing /var/www/twiki/data/Main/IpagSpectro-g2Group.txt
 - analysing /var/www/twiki/data/Main/LaogIpagsiteGroup.txt
 - analysing /var/www/twiki/data/Main/IpagAdmin-l1Group.txt
 - analysing /var/www/twiki/data/Main/IpagTheseImagerieDisqueGroup.txt
 - analysing /var/www/twiki/data/Main/IpagPlanetoGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationToupiesGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetPionierScienceGroup.txt
 - analysing /var/www/twiki/data/Main/LpgLaogCpGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatSimulationsGroup.txt
 - analysing /var/www/twiki/data/Main/LaogClGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-stflorentGroup.txt
 - analysing /var/www/twiki/data/Main/IpagIpagsiteGroup.txt
 - analysing /var/www/twiki/data/Main/LaogMarsisGroup.txt
 - analysing /var/www/twiki/data/Main/IpagDirectionScientifiqueGroup.txt
 - analysing /var/www/twiki/data/Main/IpagServicesGroup.txt
 - analysing /var/www/twiki/data/Main/IpagSherpasGroup.txt
 - analysing /var/www/twiki/data/Main/LaogTheseIfsGroup.txt
 - analysing /var/www/twiki/data/Main/IpagElectroniqueGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetSwiftsInternGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationAstrostatIPAGGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetClass0LPGroup.txt
 - analysing /var/www/twiki/data/Main/IpagChercheuraffilieGroup.txt
 - analysing /var/www/twiki/data/Main/IpagGuepardGroup.txt
 - analysing /var/www/twiki/data/Main/JmmcGroup.txt
 - analysing /var/www/twiki/data/Main/LaogGrilChercheursGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCdGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationHD97048Group.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-asaGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetConsertGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationV4046SgrGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationDescGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationVsiGravityIOGroup.txt
 - analysing /var/www/twiki/data/Main/IpagXlabuserGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetFocusExecutifGroup.txt
 - analysing /var/www/twiki/data/Main/IpagWeb-descGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSherpaGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaboration51OphiuciGroup.txt
 - analysing /var/www/twiki/data/Main/LaogAero-l1Group.txt
 - analysing /var/www/twiki/data/Main/LaogAstromolGroup.txt
 - analysing /var/www/twiki/data/Main/LaogIngetechGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationAmbBrgGroup.txt
 - analysing /var/www/twiki/data/Main/IpagExtraGroup.txt
 - analysing /var/www/twiki/data/Main/IpagSpectroGroup.txt
 - analysing /var/www/twiki/data/Main/LaogObsaulaogGroup.txt
 - analysing /var/www/twiki/data/Main/IpagRadar-l1Group.txt
 - analysing /var/www/twiki/data/Main/IpagSphereGroup.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationGravityGroup.txt
 - analysing /var/www/twiki/data/Main/IpagExtra-blueGroup.txt
 - analysing /var/www/twiki/data/Main/IpagCollaborationSpAstromGroup.txt
 - analysing /var/www/twiki/data/Main/LaogSphereGroup.txt
 - analysing /var/www/twiki/data/Main/IpagExoplanetesGroup.txt
 - analysing /var/www/twiki/data/Main/IpagSpectro-g3Group.txt
 - analysing /var/www/twiki/data/Main/LaogCollaborationImageReconstructionGroup.txt
 - analysing /var/www/twiki/data/Main/LaogFostGroup.txt
 - analysing /var/www/twiki/data/Main/LaogAdmin-l1Group.txt
 - analysing /var/www/twiki/data/Main/ProjetSphereGroup.txt
 - analysing /var/www/twiki/data/Main/LaogLpgsiteGroup.txt
 - analysing /var/www/twiki/data/Main/ProjetNeatLabDemoGroup.txt
htgroup file written into /var/www/twiki/data/.htgroups

