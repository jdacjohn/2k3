#!/usr/bin/perl -T
##
## rss_news.cgi - Get the RSS Feeds
##
## Copyright (C) 2006 2k3 Technologies
##
## $Author: Jarnold $
## $Date: 6/18/06 10:38a $
## $Revision: 2 $
## Change History:
## 04.06.2006 - Initial Version - jarnold
## 06.06.2006 - Changed to use XML::RSS and LWP::SIMPLE so it will run on 1and1's servers. - jarnold

use strict;
use lib '.';
use CGI;
use HTML::Entities;
use HTML::Template;
use XML::RSS;
use LWP::Simple;
use TWOK3::Conf;

my %Modes = (
  'default'  => \&do_default,
  'refresh'  => \&do_refresh,
);

my $Q = CGI->new();
my $C = TWOK3::Conf->new();
my %F = $Q->Vars();

my $ERRSTR = '';
our $DEBUG = 0;
our $DEBUG_INIT = 0;

## main 
$|=1;
delete @ENV{qw(PATH IFS CDPATH ENV BASH_ENV)};

if (!defined $F{'mode'}) {
  $Modes{'default'}->();
} elsif ($Modes{"$F{'mode'}"}) {
  $Modes{"$F{'mode'}"}->();
} else {
  &fatal_error('Invalid mode type');
}

exit;

#------------------------------------------------------------------------------
# Entry-point routines
#------------------------------------------------------------------------------
sub do_default {
  &get_feeds();
}

#------------------------------------------------------------------------------
# Subs
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# get_feeds() - get the feeds to display on the news page
#
# Change History:
# 04.07.2006 - Initial Version - jarnold
#------------------------------------------------------------------------------
sub get_feeds {
  my @feeds = $C->feeds();
  &debug("Size of Feeds = " . @feeds);
  #my $parser = XML::RSS::Parser->new();
  my $count = 1;
  my @channelTitles = ();
  my @channels = ();
  foreach my $uri (@feeds) {
		
		my $rss = XML::RSS->new();
		my $data = get($uri);
		$rss->parse($data);
		my $channel = $rss->{channel};
		
    my %titleref = ();
    #my $feed_title = $feed->query('/channel/title');
    %titleref->{title} = $$channel{title};
    push(@channelTitles,\%titleref);
    &debug("Channel Title = " . $$channel{title} . "<br>");
    my @items = ();
    #my $count = $feed->item_count();
    #&debug(" " . ($count) . "<br>");
    foreach my $item (@{$rss->{items}}) {
      my %itemref = ();
      my $node = $$item{'title'};
      %itemref->{title} = $node;
      &debug(" " . $node . "<br>");
      my $link = $$item{'link'};
      %itemref->{link} = $link;
      &debug("     " . $link . "<br>");
      my $description = $$item{'description'};
      %itemref->{description} = $description;
      &debug("\n" . $description . "<br>");
      push(@items,\%itemref);
    }
    my %channelContent = ();
    %channelContent->{items} = \@items;
    %channelContent->{title} = $$channel{title};
    if ($count > 1) { %channelContent->{up} = 1; }
    my $feed_image = $rss->{image};
    if ($feed_image) {
      my $imageAlt = $$channel{'title'};
      %channelContent->{'imageAlt'} = $imageAlt;
      my $imageURL = $$feed_image{'url'};
      %channelContent->{'imageUrl'} = $imageURL;
      my $imageLink = $$channel{'link'};
      %channelContent->{'imageLink'} = $imageLink;
    }
    push(@channels,\%channelContent);
    $count++;
  }
  &show_feeds(\@channelTitles,\@channels);
}

#------------------------------------------------------------------------------
# show_feeds() - Show the news page
#
# Change History:
# 04.07.2006 - Initial Version - jarnold
#------------------------------------------------------------------------------
sub show_feeds {
  my ($channelTitles,$channels) = @_;
  
  my $tmpl = $C->tmpl('news');
  $tmpl->param(channelTitles=>$channelTitles);
  $tmpl->param(channels=>$channels);
  print $Q->header();
  print $tmpl->output();
  exit;

}

#------------------------------------------------------------------------------
#  Error Reporting and Debugging 
#------------------------------------------------------------------------------
sub show_error {
  my $msg = shift;
  my $template = $C->tmpl('error_user');
  $template->param(msg=>$msg);
  print $Q->header(-type=>'text/html');
  print $template->output();
  exit;
}

sub show_success {
	my $msg = shift;
	my $template = $C->tmpl('success');
	$template->param(msg=>$msg);
	print $Q->header(-type=>'text/html');
	print $template->output;
}

sub debug_init {
  $DEBUG_INIT = 1;
  print $Q->header(-type=>'text/html');
}

sub debug {
  if ($DEBUG) {
    if (!$DEBUG_INIT) {
      debug_init();
    }
    my $msg = shift;
    print $msg;
  }
}

