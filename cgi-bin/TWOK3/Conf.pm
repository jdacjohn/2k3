package TWOK3::Conf;
##
## Conf.pm - Master configuration module
##
## Copyright (C) 2k3 Technologies, 2006
##
## $Id: Conf.pm,v 1.25 2004/03/22 05:04:44 jarnold Exp $

use strict;
use HTML::Template;
use Carp;
use HTML::Entities qw(encode_entities);

sub new { return bless {},__PACKAGE__ }

#my $HOME = '/home/2k3';
my $HOME = '/kunden/homepages/8/d166105058/htdocs/2k3';
my @feeds = (
  'http://www.foxnews.com/xmlfeed/rss/0,4313,80,00.rss',
  #'http://rss.thesmokinggun.com/rss.asp',
  #'http://www.siliconvalley.com/mld/siliconvalley/rss/rss.xml',
  #'http://www.weather.gov/alerts/wwarssget.php?zone=TXZ127',
  #'http://dwlt.net/tapestry/dilbert.rdf',
  #'http://www.rediff.com/rss/inrss.xml',
  #'http://www.quotationspage.com/data/qotd.rss',
	'http://www.theinquirer.net/inquirer.rss',
  'http://rss.topix.net/rss/tech/open-source.xml',
  'http://www.wired.com/news_drop/netcenter/netcenter.rdf',
  'http://www.webreference.com/webreference.rdf',
  #'http://www.theonion.com/content/feeds/weekly',
);

sub feeds { @feeds };

## template stuff
sub tmpl { 
	my ($self,$tmpl,$opts) = @_;
  $opts = { loop_context_vars => 1, die_on_bad_params => 1 } unless ($opts);
	my $template = HTML::Template->new(filename => "$HOME/tmpl/$tmpl.tmpl",%$opts); 
	return $template;
}

## encode form stuff
sub encode_html {
	my ($self,$F) = shift;
	foreach(keys %$F) {
		$F->{$_} = encode_entities($F->{$_});
	}
}

## clean chars from a string -- primarily used for creating files
sub sanitize_string {
	my ($self, $str) = @_;
	$str =~ s#[^a-zA-Z0-9._-]#_#g;
	$str =~ s#_+#_#;
	return $str;
}
