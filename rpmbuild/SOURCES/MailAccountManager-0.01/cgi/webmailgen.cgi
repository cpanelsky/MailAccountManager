#!/usr/bin/perl
use strict;
use CGI ; 
use LWP::UserAgent;

my $query = new CGI;
my $domainName = $query->param('domain');
my $domainUser = $query->param('mailuser');
my $mailaccount = "$domainUser"."@"."$domainName";

my $targetURL = `/usr/local/cpanel/whostmgr/docroot/cgi/addons/MailAccountManager/webmailgen.sh $mailaccount`;
sleep 1;
print "Location: $targetURL\n\n";
