#!/usr/local/cpanel/3rdparty/perl/522/bin/perl

use strict;
use Cpanel::App                ();
use Cpanel::Template           ();
use Cpanel::Config::LoadCpConf ();
use Whostmgr::ACLS             ();
use Whostmgr::HTMLInterface    ();
use File::Slurp;
use warnings;

my $mainHFileName = '/usr/local/cpanel/whostmgr/docroot/cgi/addons/MailAccountManager/includesresources.html';
my @hLines        = read_file($mainHFileName);
my $hostname      = "$ENV{HOST}";
my $session       = "$ENV{cp_security_token}";
print "Content-type: text/html\r\n\r\n\r\n";
foreach my $hLine (@hLines) {
    print $hLine ;
}

use File::Slurp qw(read_file);

#read in users from passwd
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

#for the users found, if we aren't root look for an etc dir
foreach my $user ( keys %user_list ) {
    if ( $user ne "root" ) {
        opendir( ETC, "$user_list{$user}/etc" ) || next;
        my $path    = $user_list{$user};
        my $userset = 1;

        #for the domains found in the users etc dir
        while ( my $udomain = readdir(ETC) ) {
            next if $udomain =~ /^\./;    # skip . and .. dirs

            #see if we are a valid etc domain and if so, look for mail users and print
            if ( -d "$path/etc/$udomain/" ) {
                open( $PASSWD, "$path/etc/$udomain/passwd" ) || next;
                if ( $userset == 1 ) {
                    print
                        "<tr align=right>\n<td style=\"width:505px;border-radius:2px;border-color:gray;\"><font size=4px color=white>";
                    printf( "%-16s", $user );
                    print "<font>";

                    my $apihrefpre =
                        "\r\n<a style=\"border-radius:2px;border-width:1px;text-decoration:none;margin:2px;padding:1px;background-color:#428bca;\"  href=\"../../../json-api";
                    my $apihrefmid = "target=\"_blank\"><font color=white size=4px><strong>";
                    my $apihrefend = "</strong><\/font> <\/a>\r\n";

                    print "$apihrefpre"
                        . "/suspend_outgoing_email?api.version=1&user=$user\""
                        . " $apihrefmid"
                        . "Suspend"
                        . "$apihrefend\r\n";
                    print "$apihrefpre"
                        . "/unsuspend_outgoing_email?api.version=1&user=$user\""
                        . " $apihrefmid"
                        . "Unsuspend"
                        . "$apihrefend\r\n";
                    print "$apihrefpre"
                        . "/hold_outgoing_email?api.version=1&user=$user\""
                        . " $apihrefmid"
                        . "Hold Mail"
                        . "$apihrefend\r\n";
                    print "$apihrefpre"
                        . "/release_outgoing_email?api.version=1&user=$user\""
                        . " $apihrefmid"
                        . "Release Mail"
                        . "$apihrefend\r\n";

                    print "</td></tr><td>";
                }
                $userset = 0;

                while ( my $PWLINE = <$PASSWD> ) {
                    $PWLINE =~ s/:.*//;    # only show line data before first colon (username only)
                    chomp( $udomain, $PWLINE );
                    my $sumFile = "$path/mail/$udomain/$PWLINE/maildirsize";
                    open my $SUMLINES, '<', $sumFile || continue;
                    my $total  = "0";
                    my $totals = "0";
                    $userset = 0;

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
                        "\t<div><li style=\"display:block;float:left;clear:left;\"><hr><font size=4px><strong>$mailaccount<\/font><nbsb><nbsp><nbsp>";
                    my $apihrefpre2 =
                        "<a style=\"border-radius:2px;border-width:1px;text-decoration:none;margin:2px;padding:1px;background-color:#428bca;\"  href=\"../../../json-api";

                    my $dsval = sprintf( "%06.4f", $totals );                                #print disk space
                    my $jsonuapimailpre = "$apihrefpre2" . "/cpanel?cpanel_jsonapi_user=";
                    my $jsonuapimailmid1 = "&cpanel_jsonapi_apiversion=3&cpanel_jsonapi_module=Email&cpanel_jsonapi_func=";
                    my $jsonuapimailmid2 = " target=\"_blank\"><font color=white size=3px><strong>";
                    my $jsonuapimailend  = "</strong><\/font> <\/a>";
                    my $webmailbegin =
                        "<a style=\"border-radius:2px;border-width:1px;text-decoration:none;margin:1px;padding:3px;background-color:#428bca;\"  href=\".\/webmailgen.cgi?domain=";
                    printf( "\t%-05s MB", $dsval );
                    print "<\/strong><div align=\"left\">";
                    print "$webmailbegin"
                        . "$udomain&mailuser=$PWLINE\""
                        . "$jsonuapimailmid2"
                        . "Webmail"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"
                        . "suspend_incoming&email=$mailaccount\""
                        . "$jsonuapimailmid2"
                        . "Suspend"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"
                        . "unsuspend_incoming&email=$mailaccount\""
                        . "$jsonuapimailmid2"
                        . "Unsuspend"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"
                        . "suspend_login&email=$mailaccount\""
                        . "$jsonuapimailmid2"
                        . "Suspend Login"
                        . "$jsonuapimailend\r\n";
                    print "$jsonuapimailpre" . "$user"
                        . "$jsonuapimailmid1"
                        . "suspend_login&email=$mailaccount\""
                        . "$jsonuapimailmid2"
                        . "Unsuspend Login"
                        . "$jsonuapimailend\r\n";

                    print "<\/div>";
                    print "</li><\/div>";

                }
                print "<\/td>";
                close($PASSWD);
            }
        }
    }
    close(ETC);
}
print "</div>\r\n";
print "  <\/table>\n";
print " <\/body>\n";

print "<\/html>\n";

