#!/usr/local/cpanel/3rdparty/perl/522/bin/perl

use strict;
use Cpanel::App                ();
use Cpanel::Template           ();
use Cpanel::Config::LoadCpConf ();
use Whostmgr::ACLS             ();
use Whostmgr::HTMLInterface    ();
use File::Slurp;
use warnings;

# this includes prints the static content, top of the page
my $mainHFileName = '/usr/local/cpanel/whostmgr/docroot/cgi/addons/MailAccountManager/includesresources.html';
my @hLines        = read_file($mainHFileName); #array of the lines in the file above to print from
my $hostname      = "$ENV{HOST}"; # get our hostname to use in the URL
my $session       = "$ENV{cp_security_token}"; # get our session to use in the URL
print "Content-type: text/html\r\n"; # start the http session with the daemon for the client
print "Cache-Control: no-transform\r\n\r\n\r\n";

foreach my $hLine (@hLines) { # print the lines from the resource file
    print $hLine ;
}

# some terrible things to make terrible things worse(or better?)
my $strongO = "<strong>" ; my $strongC = "</strong>";
my $divO    = "<div>"    ; my $divC    = "</div>"   ;
my $trO     = "<tr>"     ; my $trC     = "</tr>"    ;
my $tdO     = "<td>"     ; my $tdC     = "</td>"    ;
my $fontC   = "</font>"  ; my $nbs     = "&nbsp;"   ;
my $indiv   = "<div style=\"display: inline\" id=\"";
my $usercounter = 0;
my $userswmailc = 0;
my $mailaccntsc = 0;

#read in users from passwd file, check for the users in /v/c/users/, build a hash to parse
my @passwd = read_file("/etc/passwd");
my $PASSWD;
my $dir = '/var/cpanel/users';
my %user_list;
opendir( DIR, $dir ) or die $!;
while ( my $file = readdir(DIR) ) {
    next if ( $file =~ m/^\./ );
    foreach my $line (@passwd) {
        #if we look like a system and cpanel user?
        if ( $line =~ /^$file:[^:]*:[^:]*:[^:]*:[^:]*:([a-z0-9_\/]+):.*/ ) {
            $user_list{$file} = $1;
        }
    }
}
closedir(DIR);

#for the users found, look for an etc dir 
foreach my $user ( sort keys %user_list ) {
    if ( $user ne "root" ) {
        opendir( ETC, "$user_list{$user}/etc" ) || next;
        my $path    = $user_list{$user};
        my $userset = 1; 
        $usercounter++;
        #for the domains found in the users etc dir
        while ( my $udomain = readdir(ETC) ) { #get the userdomains from the users etc dir
            next if $udomain =~ /^\./;    # skip . and .. dirs
            #see if we are a valid etc domain and if so, look for mail users and print
            if ( -d "$path/etc/$udomain/" ) {   # check passwd for the mail user
                  $userswmailc++;
                 if ( -z "$path/etc/$udomain/passwd" ) {
		$userswmailc--;                 
                 }
                open( $PASSWD, "$path/etc/$udomain/passwd" ) || next;
                if ( $userset == 1 ) {
                      #check our suspension status, set toggle vars for later use
                      open(USERFILE, "/var/cpanel/users/$user") || next; 
                          my $suspendedout;
                          my $heldout;
                          while  (<USERFILE>) {
                           if ( $_ =~ /^OUTGOING_MAIL_SUSPENDED/ ) {
                             $suspendedout = $_ ;
                           }
                           if ($_ =~ /^OUTGOING_MAIL_HOLD/) {
                             $heldout = $_;
                           }
                          }
                          close USERFILE;
                     #here we print the start of our users list
                    print
                        "<tr align=left id=\"_s___$user\" >\n<td  class=usertr><font size=4px color=white>&#9899; $nbs";
                    printf( "%-16s", $user );
                    print "$tdC $trC $tdO <div  style=\"display:inline;\"> $strongO cPanel User-><\/div>";
                     #also bad, here we make the strings for the hrefs and their target URL's and the divs 
                     my $apihrefpre =
                         "\r\n<a class=\"acbuttons\"  href=\"../../../json-api";
                     my $apihrefmid = "  onClick=\"event.preventDefault();updateStatusDiv(this)\"   ><font color=white size=4px>$strongO";
                     my $apihrefend = "$strongC $fontC <\/a>\r\n";  
                     print "$apihrefpre"
                         . "/suspend_outgoing_email?api.version=1&user=$user\" id=\"asuspout_$user\"" #outgoing suspension for cPanel account
                         . " $apihrefmid"
                         . "Suspend"
                         . "$apihrefend\r\n";
                     print "$apihrefpre"
                         . "/unsuspend_outgoing_email?api.version=1&user=$user\" id=\"unsuspout_$user\" " #outgoing unsuspension for cPanel account
                         . " $apihrefmid"
                         . "Unsuspend"
                         . "$apihrefend\r\n";
                     print "$apihrefpre"
                         . "/hold_outgoing_email?api.version=1&user=$user\" id=\"holdout_$user\"" #hold outbound for cPanel account
                         . " $apihrefmid"
                         . "Hold Mail"
                        . "$apihrefend\r\n";
                     print "$apihrefpre"
                         . "/release_outgoing_email?api.version=1&user=$user\" id=\"relout_$user\""#release outbound for cpanel account
                         . " $apihrefmid"
                        . "Release Mail"
                         . "$apihrefend\r\n";
			# add some initial symbols and keys to let users know what is set based on what we found, dyanmicly updated in the button.js files
			print "$nbs";
                           print "$indiv"."susp-$user\">";                        
                         if ( defined $suspendedout  ) {
                           print "SO:&#x02A02;";
                         }
                           print " $nbs $divC ";
                           print "$indiv"."held-$user\">";
                         if (defined $heldout ) { 
			   print "H:&#9888;"; 
			}
			  print "$nbs $divC";

                      print " $divC $divC ";

                }
                $userset = 0;
                while ( my $PWLINE = <$PASSWD> ) {
                    $PWLINE =~ s/:.*//;    # only show line data before first colon (username only)
                    chomp( $udomain, $PWLINE );
                    my $sumFile = "$path/mail/$udomain/$PWLINE/maildirsize";
                    open my $SUMLINES, '<', $sumFile || continue; #mailsize
                    my $total  = "0";
                    my $totals = "0";
                    $userset = 0;
                    $mailaccntsc++;              #add more maila accounts  here
                      #getting the total disk space found in the mail quota file
                    while (<$SUMLINES>) {
                        my ( $suml, $thing ) = split;
                        if ( $suml !~ /[a-zA-Z]/ && $suml != 0 ) {
                            $totals += $suml;
                        }
                    }
                    $totals = ( $totals / 1024 / 1024 );
                    my $mailaccount = "$PWLINE\@$udomain";
                    chomp($mailaccount);
                    print
                        "\t<div id=\"_s___$mailaccount\"><li class=mali> <br style=\"line-height:3px\"> <hr><font size=4px><div id=\"$mailaccount\"> $strongO $mailaccount $fontC";
                    my $dsval = sprintf( "%06.4f", $totals );                                #print disk space
                    my $mailaccountsusp = undef;
                         if ( -e "/home/$user/etc/\.$mailaccount\.suspended_incoming" ) {  #see if we're suspended at the mail account level
                            $mailaccountsusp="1";
                         }  
                          open( MSHAD, "/home/$user/etc/$udomain/shadow" ) || next;  #see if our login is suspended
                           my $suspendedlogin;
                          while  (<MSHAD>) { 
                            if ( $_ =~ /^$PWLINE:!!/ ) {
                             $suspendedlogin = $_ ;
                            }
                           }
                           close MSHAD;
                    my $apihrefpre2      = "<a class=acbuttons href=\"../../../json-api"; #constants for html for the mail account buttons
                    my $jsonuapimailpre  = "$apihrefpre2" . "/cpanel?cpanel_jsonapi_user=";
                    my $jsonuapimailmid1 = "&cpanel_jsonapi_apiversion=3&cpanel_jsonapi_module=Email&cpanel_jsonapi_func=";
                    my $jsonuapimailmid2 = " onClick=\"event.preventDefault();updateStatusDiv(this)\"";
                    my $jsonuapimailmid3 = "><font color=white size=3px> $strongO";
                    my $jsonuapimailend  = "$strongC $fontC <\/a>";
                    my $webmailbegin     = "<a class=acbuttons  href=\".\/webmailgen.cgi?domain=";
                    printf( "\t%-05s MB", $dsval );
                    print "$strongC <br style=\"line-height:25px\">";
                    print "$webmailbegin"                # webmail button
                        . "$udomain&mailuser=$PWLINE\" target=\"_blank\" "
                        . "$jsonuapimailmid3"
                        . "Webmail"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"           # suspend incoming for mail account
                        . "suspend_incoming&email=$mailaccount\""
                        . "$jsonuapimailmid2"." id=\"msusin_$mailaccount\""
                        . "$jsonuapimailmid3"
                        . "Suspend"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"         # unsuspend incoming for mail account
                        . "unsuspend_incoming&email=$mailaccount\""
                        . "$jsonuapimailmid2"." id=\"munsusin_$mailaccount\""
                        . "$jsonuapimailmid3"
                        . "Unsuspend"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"         # suspend login for mail account
                        . "suspend_login&email=$mailaccount\""
                        . "$jsonuapimailmid2"." id=\"amsusl_$mailaccount\""
                        . "$jsonuapimailmid3"
                        . "Suspend Login"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"
                        . "unsuspend_login&email=$mailaccount\""
                        . "$jsonuapimailmid2"." id=\"munsusl_$mailaccount\""
                        . "$jsonuapimailmid3"        #unsuspend Login for mail account
                        . "Unsuspend Login"
                        . "$jsonuapimailend\r\n";
                           
                        print "$nbs $indiv"."incsusp_$mailaccount\">";
                         if ( $mailaccountsusp  ) {
                         print "SI:&#x02A02;";  # initial toggle symbols for suspend status
                           }
			print " $nbs $divC ";
                           print " $indiv"."login_$mailaccount\"> ";
                        if ( defined $suspendedlogin  ) {
                          print "L:&#9888;";
                         }
                    print "$nbs $divC $divO $divC </li>$divC";

                }
                print "$tdC";
                close($PASSWD);
            }
        }
    }
    close(ETC);
}
print "$divC\r\n";
print "  <\/table>\n";#end of our accounts table
print "<table style=\"width:200px;position:absolute;top:-9px;left:735px;\"><tr><th></th><th></th></tr>";#table for mail account stats
print "<tr><td align=right>Users w/Mail Accounts:</td><td align=right>$userswmailc</td></tr><tr><td align=right>Total User Accounts:</td><td align=right>$usercounter</td></tr><tr><td align=right>Total Mail Accounts:</td><td align=right>$mailaccntsc</td></tr><\/table>";
print "<ul class=white id=\"ourul\" style=\"visibility:hidden;position:fixed;top:50px;left:370px;transform: rotate(180deg);\"><font color=white>";#ul for search bar li items
print "</font><\/ul>";
print "<div style=\"position:fixed;top:-5px;left:538px;\" id=\"recordstoggle\"><button class=rbuttons onclick=\"showAll()\">ShowAll</button><button class=rbuttons onclick=\"hideAll();\">HideAll</button></div> ";#show/hide
print "<ul id=notifications class=white style=\"width:230px;position:fixed;top:95px;left:735px;visibility:hidden;background-color:#428bca;border-radius:1px;padding:7px;margin:5px;box-shadow: 3px 3px 15px #204060;transform:rotate(180deg);\"></ul>";
print "<script type=\"text/javascript\"> var ids = document.querySelectorAll(\'[id]\'); </script>";#initialize our array for the search bar 
print "<script src=\"buttons.js\" ></script>";#handles the API requests/returns, toggles for status
print "<script src=\"search.js\" ></script>"; #search input
print " <\/body>\n<\/html>";
