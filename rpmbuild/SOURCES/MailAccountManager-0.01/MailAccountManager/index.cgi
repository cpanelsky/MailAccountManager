#!/usr/local/cpanel/3rdparty/bin/perl
use strict;

use Cpanel::App                ();
use Cpanel::Template           ();
use Cpanel::Config::LoadCpConf ();
use Whostmgr::ACLS             ();

Whostmgr::ACLS::init_acls();

$Cpanel::App::appname = 'whostmgr';

print "Content-type: text/html\r\n\r\n";

my $cpconf_ref = Cpanel::Config::LoadCpConf::loadcpconf();

#This is redundent since we are validating ACLS elsewhere as well
#if ( !Whostmgr::ACLS::hasroot() || !$cpconf_ref->{'mailaccountmanager'} ) {
#    print "Access Denied\n";
#    exit;
#}

Cpanel::Template::process_template(
    'whostmgr',
    {
        'template_file' => 'mailaccountmanager.tmpl',
    },
);

