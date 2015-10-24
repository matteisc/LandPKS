-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.24 - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.2.0.4947
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for apex
DROP DATABASE IF EXISTS `apex`;
CREATE DATABASE IF NOT EXISTS `apex` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `apex`;


-- Dumping structure for table apex.actions
DROP TABLE IF EXISTS `actions`;
CREATE TABLE IF NOT EXISTS `actions` (
  `aid` varchar(255) NOT NULL DEFAULT '0' COMMENT 'Primary Key: Unique actions ID.',
  `type` varchar(32) NOT NULL DEFAULT '' COMMENT 'The object that that action acts on (node, user, comment, system or custom types.)',
  `callback` varchar(255) NOT NULL DEFAULT '' COMMENT 'The callback function that executes when the action runs.',
  `parameters` longblob NOT NULL COMMENT 'Parameters to be passed to the callback function.',
  `label` varchar(255) NOT NULL DEFAULT '0' COMMENT 'Label of the action.',
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores action information.';

-- Data exporting was unselected.


-- Dumping structure for table apex.authcache_p13n_key_value
DROP TABLE IF EXISTS `authcache_p13n_key_value`;
CREATE TABLE IF NOT EXISTS `authcache_p13n_key_value` (
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique key name.',
  `collection` varchar(63) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique collection name.',
  `value` longblob COMMENT 'Serialized data.',
  PRIMARY KEY (`name`,`collection`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Generic key-value store for caching things not separated...';

-- Data exporting was unselected.


-- Dumping structure for table apex.authmap
DROP TABLE IF EXISTS `authmap`;
CREATE TABLE IF NOT EXISTS `authmap` (
  `aid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique authmap ID.',
  `uid` int(11) NOT NULL DEFAULT '0' COMMENT 'User’s users.uid.',
  `authname` varchar(128) NOT NULL DEFAULT '' COMMENT 'Unique authentication name.',
  `module` varchar(128) NOT NULL DEFAULT '' COMMENT 'Module which is controlling the authentication.',
  PRIMARY KEY (`aid`),
  UNIQUE KEY `authname` (`authname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores distributed authentication mapping.';

-- Data exporting was unselected.


-- Dumping structure for table apex.batch
DROP TABLE IF EXISTS `batch`;
CREATE TABLE IF NOT EXISTS `batch` (
  `bid` int(10) unsigned NOT NULL COMMENT 'Primary Key: Unique batch ID.',
  `token` varchar(64) NOT NULL COMMENT 'A string token generated against the current user’s session id and the batch id, used to ensure that only the user who submitted the batch can effectively access it.',
  `timestamp` int(11) NOT NULL COMMENT 'A Unix timestamp indicating when this batch was submitted for processing. Stale batches are purged at cron time.',
  `batch` longblob COMMENT 'A serialized array containing the processing data for the batch.',
  PRIMARY KEY (`bid`),
  KEY `token` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores details about batches (processes that run in...';

-- Data exporting was unselected.


-- Dumping structure for table apex.block
DROP TABLE IF EXISTS `block`;
CREATE TABLE IF NOT EXISTS `block` (
  `bid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique block ID.',
  `module` varchar(64) NOT NULL DEFAULT '' COMMENT 'The module from which the block originates; for example, ’user’ for the Who’s Online block, and ’block’ for any custom blocks.',
  `delta` varchar(32) NOT NULL DEFAULT '0' COMMENT 'Unique ID for block within a module.',
  `theme` varchar(64) NOT NULL DEFAULT '' COMMENT 'The theme under which the block settings apply.',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Block enabled status. (1 = enabled, 0 = disabled)',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'Block weight within region.',
  `region` varchar(64) NOT NULL DEFAULT '' COMMENT 'Theme region within which the block is set.',
  `custom` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Flag to indicate how users may control visibility of the block. (0 = Users cannot control, 1 = On by default, but can be hidden, 2 = Hidden by default, but can be shown)',
  `visibility` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Flag to indicate how to show blocks on pages. (0 = Show on all pages except listed pages, 1 = Show only on listed pages, 2 = Use custom PHP code to determine visibility)',
  `pages` text NOT NULL COMMENT 'Contents of the "Pages" block; contains either a list of paths on which to include/exclude the block or PHP code, depending on "visibility" setting.',
  `title` varchar(64) NOT NULL DEFAULT '' COMMENT 'Custom title for the block. (Empty string will use block default title, <none> will remove the title, text will cause block to use specified title.)',
  `cache` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'Binary flag to indicate block cache mode. (-2: Custom cache, -1: Do not cache, 1: Cache per role, 2: Cache per user, 4: Cache per page, 8: Block cache global) See DRUPAL_CACHE_* constants in ../includes/common.inc for more detailed information.',
  PRIMARY KEY (`bid`),
  UNIQUE KEY `tmd` (`theme`,`module`,`delta`),
  KEY `list` (`theme`,`status`,`region`,`weight`,`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores block settings, such as region and visibility...';

-- Data exporting was unselected.


-- Dumping structure for table apex.blocked_ips
DROP TABLE IF EXISTS `blocked_ips`;
CREATE TABLE IF NOT EXISTS `blocked_ips` (
  `iid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: unique ID for IP addresses.',
  `ip` varchar(40) NOT NULL DEFAULT '' COMMENT 'IP address',
  PRIMARY KEY (`iid`),
  KEY `blocked_ip` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores blocked IP addresses.';

-- Data exporting was unselected.


-- Dumping structure for table apex.block_custom
DROP TABLE IF EXISTS `block_custom`;
CREATE TABLE IF NOT EXISTS `block_custom` (
  `bid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The block’s block.bid.',
  `body` longtext COMMENT 'Block contents.',
  `info` varchar(128) NOT NULL DEFAULT '' COMMENT 'Block description.',
  `format` varchar(255) DEFAULT NULL COMMENT 'The filter_format.format of the block body.',
  PRIMARY KEY (`bid`),
  UNIQUE KEY `info` (`info`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores contents of custom-made blocks.';

-- Data exporting was unselected.


-- Dumping structure for table apex.block_node_type
DROP TABLE IF EXISTS `block_node_type`;
CREATE TABLE IF NOT EXISTS `block_node_type` (
  `module` varchar(64) NOT NULL COMMENT 'The block’s origin module, from block.module.',
  `delta` varchar(32) NOT NULL COMMENT 'The block’s unique delta within module, from block.delta.',
  `type` varchar(32) NOT NULL COMMENT 'The machine-readable name of this type from node_type.type.',
  PRIMARY KEY (`module`,`delta`,`type`),
  KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Sets up display criteria for blocks based on content types';

-- Data exporting was unselected.


-- Dumping structure for table apex.block_role
DROP TABLE IF EXISTS `block_role`;
CREATE TABLE IF NOT EXISTS `block_role` (
  `module` varchar(64) NOT NULL COMMENT 'The block’s origin module, from block.module.',
  `delta` varchar(32) NOT NULL COMMENT 'The block’s unique delta within module, from block.delta.',
  `rid` int(10) unsigned NOT NULL COMMENT 'The user’s role ID from users_roles.rid.',
  PRIMARY KEY (`module`,`delta`,`rid`),
  KEY `rid` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Sets up access permissions for blocks based on user roles';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache
DROP TABLE IF EXISTS `cache`;
CREATE TABLE IF NOT EXISTS `cache` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Generic cache table for caching things not separated out...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_admin_menu
DROP TABLE IF EXISTS `cache_admin_menu`;
CREATE TABLE IF NOT EXISTS `cache_admin_menu` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for Administration menu to store client-side...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_authcache_debug
DROP TABLE IF EXISTS `cache_authcache_debug`;
CREATE TABLE IF NOT EXISTS `cache_authcache_debug` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for authcache debug.';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_authcache_key
DROP TABLE IF EXISTS `cache_authcache_key`;
CREATE TABLE IF NOT EXISTS `cache_authcache_key` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for mapping sessions to authcache keys.';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_authcache_p13n
DROP TABLE IF EXISTS `cache_authcache_p13n`;
CREATE TABLE IF NOT EXISTS `cache_authcache_p13n` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for authcache p13n.';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_block
DROP TABLE IF EXISTS `cache_block`;
CREATE TABLE IF NOT EXISTS `cache_block` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for the Block module to store already built...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_bootstrap
DROP TABLE IF EXISTS `cache_bootstrap`;
CREATE TABLE IF NOT EXISTS `cache_bootstrap` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for data required to bootstrap Drupal, may be...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_field
DROP TABLE IF EXISTS `cache_field`;
CREATE TABLE IF NOT EXISTS `cache_field` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Generic cache table for caching things not separated out...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_filter
DROP TABLE IF EXISTS `cache_filter`;
CREATE TABLE IF NOT EXISTS `cache_filter` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for the Filter module to store already...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_form
DROP TABLE IF EXISTS `cache_form`;
CREATE TABLE IF NOT EXISTS `cache_form` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for the form system to store recently built...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_image
DROP TABLE IF EXISTS `cache_image`;
CREATE TABLE IF NOT EXISTS `cache_image` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table used to store information about image...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_libraries
DROP TABLE IF EXISTS `cache_libraries`;
CREATE TABLE IF NOT EXISTS `cache_libraries` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table to store library information.';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_menu
DROP TABLE IF EXISTS `cache_menu`;
CREATE TABLE IF NOT EXISTS `cache_menu` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for the menu system to store router...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_page
DROP TABLE IF EXISTS `cache_page`;
CREATE TABLE IF NOT EXISTS `cache_page` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table used to store compressed pages for anonymous...';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_path
DROP TABLE IF EXISTS `cache_path`;
CREATE TABLE IF NOT EXISTS `cache_path` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for path alias lookup.';

-- Data exporting was unselected.


-- Dumping structure for table apex.cache_update
DROP TABLE IF EXISTS `cache_update`;
CREATE TABLE IF NOT EXISTS `cache_update` (
  `cid` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique cache ID.',
  `data` longblob COMMENT 'A collection of data to cache.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry should expire, or 0 for never.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when the cache entry was created.',
  `serialized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate whether content is serialized (1) or not (0).',
  PRIMARY KEY (`cid`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cache table for the Update module to store information...';

-- Data exporting was unselected.


-- Dumping structure for table apex.ckeditor_input_format
DROP TABLE IF EXISTS `ckeditor_input_format`;
CREATE TABLE IF NOT EXISTS `ckeditor_input_format` (
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT 'Name of the CKEditor role',
  `format` varchar(128) NOT NULL DEFAULT '' COMMENT 'Drupal filter format ID',
  PRIMARY KEY (`name`,`format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores CKEditor input format assignments';

-- Data exporting was unselected.


-- Dumping structure for table apex.ckeditor_settings
DROP TABLE IF EXISTS `ckeditor_settings`;
CREATE TABLE IF NOT EXISTS `ckeditor_settings` (
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT 'Name of the CKEditor profile',
  `settings` text COMMENT 'Profile settings',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores CKEditor profile settings';

-- Data exporting was unselected.


-- Dumping structure for table apex.comment
DROP TABLE IF EXISTS `comment`;
CREATE TABLE IF NOT EXISTS `comment` (
  `cid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique comment ID.',
  `pid` int(11) NOT NULL DEFAULT '0' COMMENT 'The comment.cid to which this comment is a reply. If set to 0, this comment is not a reply to an existing comment.',
  `nid` int(11) NOT NULL DEFAULT '0' COMMENT 'The node.nid to which this comment is a reply.',
  `uid` int(11) NOT NULL DEFAULT '0' COMMENT 'The users.uid who authored the comment. If set to 0, this comment was created by an anonymous user.',
  `subject` varchar(64) NOT NULL DEFAULT '' COMMENT 'The comment title.',
  `hostname` varchar(128) NOT NULL DEFAULT '' COMMENT 'The author’s host name.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'The time that the comment was created, as a Unix timestamp.',
  `changed` int(11) NOT NULL DEFAULT '0' COMMENT 'The time that the comment was last edited, as a Unix timestamp.',
  `status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'The published status of a comment. (0 = Not Published, 1 = Published)',
  `thread` varchar(255) NOT NULL COMMENT 'The vancode representation of the comment’s place in a thread.',
  `name` varchar(60) DEFAULT NULL COMMENT 'The comment author’s name. Uses users.name if the user is logged in, otherwise uses the value typed into the comment form.',
  `mail` varchar(64) DEFAULT NULL COMMENT 'The comment author’s e-mail address from the comment form, if user is anonymous, and the ’Anonymous users may/must leave their contact information’ setting is turned on.',
  `homepage` varchar(255) DEFAULT NULL COMMENT 'The comment author’s home page address from the comment form, if user is anonymous, and the ’Anonymous users may/must leave their contact information’ setting is turned on.',
  `language` varchar(12) NOT NULL DEFAULT '' COMMENT 'The languages.language of this comment.',
  PRIMARY KEY (`cid`),
  KEY `comment_status_pid` (`pid`,`status`),
  KEY `comment_num_new` (`nid`,`status`,`created`,`cid`,`thread`),
  KEY `comment_uid` (`uid`),
  KEY `comment_nid_language` (`nid`,`language`),
  KEY `comment_created` (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores comments and associated data.';

-- Data exporting was unselected.


-- Dumping structure for table apex.ctools_css_cache
DROP TABLE IF EXISTS `ctools_css_cache`;
CREATE TABLE IF NOT EXISTS `ctools_css_cache` (
  `cid` varchar(128) NOT NULL COMMENT 'The CSS ID this cache object belongs to.',
  `filename` varchar(255) DEFAULT NULL COMMENT 'The filename this CSS is stored in.',
  `css` longtext COMMENT 'CSS being stored.',
  `filter` tinyint(4) DEFAULT NULL COMMENT 'Whether or not this CSS needs to be filtered.',
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='A special cache used to store CSS that must be non-volatile.';

-- Data exporting was unselected.


-- Dumping structure for table apex.ctools_object_cache
DROP TABLE IF EXISTS `ctools_object_cache`;
CREATE TABLE IF NOT EXISTS `ctools_object_cache` (
  `sid` varchar(64) NOT NULL COMMENT 'The session ID this cache object belongs to.',
  `name` varchar(128) NOT NULL COMMENT 'The name of the object this cache is attached to.',
  `obj` varchar(128) NOT NULL COMMENT 'The type of the object this cache is attached to; this essentially represents the owner so that several sub-systems can use this cache.',
  `updated` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The time this cache was created or updated.',
  `data` longblob COMMENT 'Serialized data being stored.',
  PRIMARY KEY (`sid`,`obj`,`name`),
  KEY `updated` (`updated`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='A special cache used to store objects that are being...';

-- Data exporting was unselected.


-- Dumping structure for table apex.date_formats
DROP TABLE IF EXISTS `date_formats`;
CREATE TABLE IF NOT EXISTS `date_formats` (
  `dfid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The date format identifier.',
  `format` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'The date format string.',
  `type` varchar(64) NOT NULL COMMENT 'The date format type, e.g. medium.',
  `locked` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Whether or not this format can be modified.',
  PRIMARY KEY (`dfid`),
  UNIQUE KEY `formats` (`format`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores configured date formats.';

-- Data exporting was unselected.


-- Dumping structure for table apex.date_format_locale
DROP TABLE IF EXISTS `date_format_locale`;
CREATE TABLE IF NOT EXISTS `date_format_locale` (
  `format` varchar(100) NOT NULL COMMENT 'The date format string.',
  `type` varchar(64) NOT NULL COMMENT 'The date format type, e.g. medium.',
  `language` varchar(12) NOT NULL COMMENT 'A languages.language for this format to be used with.',
  PRIMARY KEY (`type`,`language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores configured date formats for each locale.';

-- Data exporting was unselected.


-- Dumping structure for table apex.date_format_type
DROP TABLE IF EXISTS `date_format_type`;
CREATE TABLE IF NOT EXISTS `date_format_type` (
  `type` varchar(64) NOT NULL COMMENT 'The date format type, e.g. medium.',
  `title` varchar(255) NOT NULL COMMENT 'The human readable name of the format type.',
  `locked` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Whether or not this is a system provided format.',
  PRIMARY KEY (`type`),
  KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores configured date format types.';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_config
DROP TABLE IF EXISTS `field_config`;
CREATE TABLE IF NOT EXISTS `field_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'The primary identifier for a field',
  `field_name` varchar(32) NOT NULL COMMENT 'The name of this field. Non-deleted field names are unique, but multiple deleted fields can have the same name.',
  `type` varchar(128) NOT NULL COMMENT 'The type of this field.',
  `module` varchar(128) NOT NULL DEFAULT '' COMMENT 'The module that implements the field type.',
  `active` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether the module that implements the field type is enabled.',
  `storage_type` varchar(128) NOT NULL COMMENT 'The storage backend for the field.',
  `storage_module` varchar(128) NOT NULL DEFAULT '' COMMENT 'The module that implements the storage backend.',
  `storage_active` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether the module that implements the storage backend is enabled.',
  `locked` tinyint(4) NOT NULL DEFAULT '0' COMMENT '@TODO',
  `data` longblob NOT NULL COMMENT 'Serialized data containing the field properties that do not warrant a dedicated column.',
  `cardinality` tinyint(4) NOT NULL DEFAULT '0',
  `translatable` tinyint(4) NOT NULL DEFAULT '0',
  `deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `field_name` (`field_name`),
  KEY `active` (`active`),
  KEY `storage_active` (`storage_active`),
  KEY `deleted` (`deleted`),
  KEY `module` (`module`),
  KEY `storage_module` (`storage_module`),
  KEY `type` (`type`),
  KEY `storage_type` (`storage_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table apex.field_config_instance
DROP TABLE IF EXISTS `field_config_instance`;
CREATE TABLE IF NOT EXISTS `field_config_instance` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'The primary identifier for a field instance',
  `field_id` int(11) NOT NULL COMMENT 'The identifier of the field attached by this instance',
  `field_name` varchar(32) NOT NULL DEFAULT '',
  `entity_type` varchar(32) NOT NULL DEFAULT '',
  `bundle` varchar(128) NOT NULL DEFAULT '',
  `data` longblob NOT NULL,
  `deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `field_name_bundle` (`field_name`,`entity_type`,`bundle`),
  KEY `deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table apex.field_data_body
DROP TABLE IF EXISTS `field_data_body`;
CREATE TABLE IF NOT EXISTS `field_data_body` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned DEFAULT NULL COMMENT 'The entity revision id this data is attached to, or NULL if the entity type is not versioned',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `body_value` longtext,
  `body_summary` longtext,
  `body_format` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`entity_type`,`entity_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `body_format` (`body_format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Data storage for field 4 (body)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_data_comment_body
DROP TABLE IF EXISTS `field_data_comment_body`;
CREATE TABLE IF NOT EXISTS `field_data_comment_body` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned DEFAULT NULL COMMENT 'The entity revision id this data is attached to, or NULL if the entity type is not versioned',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `comment_body_value` longtext,
  `comment_body_format` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`entity_type`,`entity_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `comment_body_format` (`comment_body_format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Data storage for field 1 (comment_body)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_data_field_landpks_content
DROP TABLE IF EXISTS `field_data_field_landpks_content`;
CREATE TABLE IF NOT EXISTS `field_data_field_landpks_content` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned DEFAULT NULL COMMENT 'The entity revision id this data is attached to, or NULL if the entity type is not versioned',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `field_landpks_content_url` varchar(1024) DEFAULT NULL,
  `field_landpks_content_title` varchar(255) DEFAULT NULL,
  `field_landpks_content_class` varchar(255) DEFAULT NULL,
  `field_landpks_content_width` varchar(4) DEFAULT NULL,
  `field_landpks_content_height` varchar(4) DEFAULT NULL,
  `field_landpks_content_frameborder` tinyint(4) NOT NULL DEFAULT '0',
  `field_landpks_content_scrolling` varchar(4) NOT NULL DEFAULT 'auto',
  `field_landpks_content_transparency` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`entity_type`,`entity_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Data storage for field 3 (field_landpks_content)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_data_filedepot_folder_desc
DROP TABLE IF EXISTS `field_data_filedepot_folder_desc`;
CREATE TABLE IF NOT EXISTS `field_data_filedepot_folder_desc` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned DEFAULT NULL COMMENT 'The entity revision id this data is attached to, or NULL if the entity type is not versioned',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `filedepot_folder_desc_value` longtext,
  `filedepot_folder_desc_format` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`entity_type`,`entity_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `filedepot_folder_desc_format` (`filedepot_folder_desc_format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Data storage for field 6 (filedepot_folder_desc)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_data_filedepot_folder_file
DROP TABLE IF EXISTS `field_data_filedepot_folder_file`;
CREATE TABLE IF NOT EXISTS `field_data_filedepot_folder_file` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned DEFAULT NULL COMMENT 'The entity revision id this data is attached to, or NULL if the entity type is not versioned',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `filedepot_folder_file_fid` int(10) unsigned DEFAULT NULL COMMENT 'The file_managed.fid being referenced in this field.',
  `filedepot_folder_file_display` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'Flag to control whether this file should be displayed when viewing content.',
  `filedepot_folder_file_description` text COMMENT 'A description of the file.',
  PRIMARY KEY (`entity_type`,`entity_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `filedepot_folder_file_fid` (`filedepot_folder_file_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Data storage for field 5 (filedepot_folder_file)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_revision_body
DROP TABLE IF EXISTS `field_revision_body`;
CREATE TABLE IF NOT EXISTS `field_revision_body` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned NOT NULL COMMENT 'The entity revision id this data is attached to',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `body_value` longtext,
  `body_summary` longtext,
  `body_format` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`entity_type`,`entity_id`,`revision_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `body_format` (`body_format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Revision archive storage for field 4 (body)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_revision_comment_body
DROP TABLE IF EXISTS `field_revision_comment_body`;
CREATE TABLE IF NOT EXISTS `field_revision_comment_body` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned NOT NULL COMMENT 'The entity revision id this data is attached to',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `comment_body_value` longtext,
  `comment_body_format` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`entity_type`,`entity_id`,`revision_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `comment_body_format` (`comment_body_format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Revision archive storage for field 1 (comment_body)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_revision_field_landpks_content
DROP TABLE IF EXISTS `field_revision_field_landpks_content`;
CREATE TABLE IF NOT EXISTS `field_revision_field_landpks_content` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned NOT NULL COMMENT 'The entity revision id this data is attached to',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `field_landpks_content_url` varchar(1024) DEFAULT NULL,
  `field_landpks_content_title` varchar(255) DEFAULT NULL,
  `field_landpks_content_class` varchar(255) DEFAULT NULL,
  `field_landpks_content_width` varchar(4) DEFAULT NULL,
  `field_landpks_content_height` varchar(4) DEFAULT NULL,
  `field_landpks_content_frameborder` tinyint(4) NOT NULL DEFAULT '0',
  `field_landpks_content_scrolling` varchar(4) NOT NULL DEFAULT 'auto',
  `field_landpks_content_transparency` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`entity_type`,`entity_id`,`revision_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Revision archive storage for field 3 (field_landpks_content)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_revision_filedepot_folder_desc
DROP TABLE IF EXISTS `field_revision_filedepot_folder_desc`;
CREATE TABLE IF NOT EXISTS `field_revision_filedepot_folder_desc` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned NOT NULL COMMENT 'The entity revision id this data is attached to',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `filedepot_folder_desc_value` longtext,
  `filedepot_folder_desc_format` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`entity_type`,`entity_id`,`revision_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `filedepot_folder_desc_format` (`filedepot_folder_desc_format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Revision archive storage for field 6 (filedepot_folder_desc)';

-- Data exporting was unselected.


-- Dumping structure for table apex.field_revision_filedepot_folder_file
DROP TABLE IF EXISTS `field_revision_filedepot_folder_file`;
CREATE TABLE IF NOT EXISTS `field_revision_filedepot_folder_file` (
  `entity_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'The entity type this data is attached to',
  `bundle` varchar(128) NOT NULL DEFAULT '' COMMENT 'The field instance bundle to which this row belongs, used when deleting a field instance',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this data item has been deleted',
  `entity_id` int(10) unsigned NOT NULL COMMENT 'The entity id this data is attached to',
  `revision_id` int(10) unsigned NOT NULL COMMENT 'The entity revision id this data is attached to',
  `language` varchar(32) NOT NULL DEFAULT '' COMMENT 'The language for this data item.',
  `delta` int(10) unsigned NOT NULL COMMENT 'The sequence number for this data item, used for multi-value fields',
  `filedepot_folder_file_fid` int(10) unsigned DEFAULT NULL COMMENT 'The file_managed.fid being referenced in this field.',
  `filedepot_folder_file_display` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'Flag to control whether this file should be displayed when viewing content.',
  `filedepot_folder_file_description` text COMMENT 'A description of the file.',
  PRIMARY KEY (`entity_type`,`entity_id`,`revision_id`,`deleted`,`delta`,`language`),
  KEY `entity_type` (`entity_type`),
  KEY `bundle` (`bundle`),
  KEY `deleted` (`deleted`),
  KEY `entity_id` (`entity_id`),
  KEY `revision_id` (`revision_id`),
  KEY `language` (`language`),
  KEY `filedepot_folder_file_fid` (`filedepot_folder_file_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Revision archive storage for field 5 (filedepot_folder_file)';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_access
DROP TABLE IF EXISTS `filedepot_access`;
CREATE TABLE IF NOT EXISTS `filedepot_access` (
  `accid` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `catid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `permid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `permtype` varchar(8) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `view` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `upload` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `upload_direct` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `upload_ver` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `approval` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `admin` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`accid`),
  KEY `catid` (`catid`),
  KEY `permid` (`permid`),
  KEY `permtype` (`permtype`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='filedepot Access Rights - for user or group access to...';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_categories
DROP TABLE IF EXISTS `filedepot_categories`;
CREATE TABLE IF NOT EXISTS `filedepot_categories` (
  `cid` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `pid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `nid` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `vid` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `group_nid` int(11) NOT NULL DEFAULT '0' COMMENT 'Used with OG mode to set the group root folder',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `description` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `folderorder` smallint(6) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `last_modified_date` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `last_updated_date` int(11) NOT NULL DEFAULT '0' COMMENT 'Used to signify if this directory has been changed in any way (including adding a new file into it)',
  PRIMARY KEY (`cid`),
  KEY `nid` (`nid`,`vid`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_downloads
DROP TABLE IF EXISTS `filedepot_downloads`;
CREATE TABLE IF NOT EXISTS `filedepot_downloads` (
  `uid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `fid` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `remote_ip` varchar(50) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `date` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  KEY `date` (`date`),
  KEY `fid` (`fid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_export_queue
DROP TABLE IF EXISTS `filedepot_export_queue`;
CREATE TABLE IF NOT EXISTS `filedepot_export_queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `orig_filename` varchar(150) NOT NULL COMMENT 'TODO: please describe this field!',
  `token` varchar(20) NOT NULL COMMENT 'TODO: please describe this field!',
  `extension` varchar(10) NOT NULL COMMENT 'TODO: please describe this field!',
  `timestamp` int(11) NOT NULL COMMENT 'TODO: please describe this field!',
  `uid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `fid` int(11) NOT NULL COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_favorites
DROP TABLE IF EXISTS `filedepot_favorites`;
CREATE TABLE IF NOT EXISTS `filedepot_favorites` (
  `uid` mediumint(9) NOT NULL COMMENT 'TODO: please describe this field!',
  `fid` int(11) NOT NULL COMMENT 'TODO: please describe this field!',
  KEY `topic_id` (`fid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_files
DROP TABLE IF EXISTS `filedepot_files`;
CREATE TABLE IF NOT EXISTS `filedepot_files` (
  `fid` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `cid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `fname` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `title` varchar(128) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `description` longtext COMMENT 'TODO: please describe this field!',
  `version` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'TODO: please describe this field!',
  `fileorder` smallint(6) NOT NULL DEFAULT '0' COMMENT 'File order in the folder',
  `drupal_fid` int(11) NOT NULL DEFAULT '0' COMMENT 'Drupal file id also called fid in the drupal tables',
  `size` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `mimetype` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `extension` varchar(8) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `submitter` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `date` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `version_ctl` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `status_changedby_uid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`fid`),
  KEY `cid` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_filesubmissions
DROP TABLE IF EXISTS `filedepot_filesubmissions`;
CREATE TABLE IF NOT EXISTS `filedepot_filesubmissions` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `fid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `cid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `fname` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `tempname` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `title` varchar(128) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `description` longtext NOT NULL COMMENT 'TODO: please describe this field!',
  `drupal_fid` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `tags` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `version` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'TODO: please describe this field!',
  `version_note` longtext NOT NULL COMMENT 'TODO: please describe this field!',
  `size` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `mimetype` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `extension` varchar(8) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `submitter` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `date` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `version_ctl` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `notify` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'TODO: please describe this field!',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`),
  KEY `cid` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_fileversions
DROP TABLE IF EXISTS `filedepot_fileversions`;
CREATE TABLE IF NOT EXISTS `filedepot_fileversions` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `fid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `fname` varchar(255) NOT NULL DEFAULT '' COMMENT 'TODO: please describe this field!',
  `version` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `drupal_fid` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `size` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `notes` longtext NOT NULL COMMENT 'TODO: please describe this field!',
  `date` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `uid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`),
  KEY `fid` (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_folderindex
DROP TABLE IF EXISTS `filedepot_folderindex`;
CREATE TABLE IF NOT EXISTS `filedepot_folderindex` (
  `cid` mediumint(9) NOT NULL COMMENT 'Folder or category ID',
  `uid` mediumint(9) NOT NULL COMMENT 'User ID',
  `folderprefix` varchar(255) DEFAULT '' COMMENT 'Folder index base value',
  KEY `cid` (`cid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Maintains the folder index for each user';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_import_queue
DROP TABLE IF EXISTS `filedepot_import_queue`;
CREATE TABLE IF NOT EXISTS `filedepot_import_queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `orig_filename` varchar(150) NOT NULL COMMENT 'TODO: please describe this field!',
  `queue_filename` varchar(255) NOT NULL COMMENT 'TODO: please describe this field!',
  `drupal_fid` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `timestamp` int(11) NOT NULL COMMENT 'TODO: please describe this field!',
  `uid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `mimetype` varchar(128) DEFAULT NULL COMMENT 'TODO: please describe this field!',
  `size` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `description` varchar(255) DEFAULT NULL COMMENT 'TODO: please describe this field!',
  `version_note` varchar(255) DEFAULT NULL COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_notificationlog
DROP TABLE IF EXISTS `filedepot_notificationlog`;
CREATE TABLE IF NOT EXISTS `filedepot_notificationlog` (
  `target_uid` mediumint(9) NOT NULL COMMENT 'TODO: please describe this field!',
  `submitter_uid` mediumint(9) NOT NULL COMMENT 'TODO: please describe this field!',
  `notification_type` tinyint(4) NOT NULL COMMENT 'TODO: please describe this field!',
  `fid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `cid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `datetime` int(11) NOT NULL COMMENT 'TODO: please describe this field!',
  KEY `target_uid` (`target_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_notifications
DROP TABLE IF EXISTS `filedepot_notifications`;
CREATE TABLE IF NOT EXISTS `filedepot_notifications` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `fid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `ignore_filechanges` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `cid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `cid_newfiles` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `cid_changes` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `uid` mediumint(9) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  `date` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`),
  KEY `cid` (`cid`),
  KEY `fid` (`fid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_recentfolders
DROP TABLE IF EXISTS `filedepot_recentfolders`;
CREATE TABLE IF NOT EXISTS `filedepot_recentfolders` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `uid` mediumint(9) NOT NULL COMMENT 'TODO: please describe this field!',
  `cid` mediumint(9) NOT NULL COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`),
  KEY `cid` (`cid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.filedepot_usersettings
DROP TABLE IF EXISTS `filedepot_usersettings`;
CREATE TABLE IF NOT EXISTS `filedepot_usersettings` (
  `uid` mediumint(9) NOT NULL COMMENT 'TODO: please describe this field!',
  `notify_newfile` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'TODO: please describe this field!',
  `notify_changedfile` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'TODO: please describe this field!',
  `allow_broadcasts` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'TODO: please describe this field!',
  `allowable_view_folders` text NOT NULL COMMENT 'TODO: please describe this field!',
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.file_managed
DROP TABLE IF EXISTS `file_managed`;
CREATE TABLE IF NOT EXISTS `file_managed` (
  `fid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'File ID.',
  `uid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The users.uid of the user who is associated with the file.',
  `filename` varchar(255) NOT NULL DEFAULT '' COMMENT 'Name of the file with no path components. This may differ from the basename of the URI if the file is renamed to avoid overwriting an existing file.',
  `uri` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT 'The URI to access the file (either local or remote).',
  `filemime` varchar(255) NOT NULL DEFAULT '' COMMENT 'The file’s MIME type.',
  `filesize` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT 'The size of the file in bytes.',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A field indicating the status of the file. Two status are defined in core: temporary (0) and permanent (1). Temporary files older than DRUPAL_MAXIMUM_TEMP_FILE_AGE will be removed during a cron run.',
  `timestamp` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'UNIX timestamp for when the file was added.',
  PRIMARY KEY (`fid`),
  UNIQUE KEY `uri` (`uri`),
  KEY `uid` (`uid`),
  KEY `status` (`status`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores information for uploaded files.';

-- Data exporting was unselected.


-- Dumping structure for table apex.file_usage
DROP TABLE IF EXISTS `file_usage`;
CREATE TABLE IF NOT EXISTS `file_usage` (
  `fid` int(10) unsigned NOT NULL COMMENT 'File ID.',
  `module` varchar(255) NOT NULL DEFAULT '' COMMENT 'The name of the module that is using the file.',
  `type` varchar(64) NOT NULL DEFAULT '' COMMENT 'The name of the object type in which the file is used.',
  `id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The primary key of the object using the file.',
  `count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The number of times this file is used by this object.',
  PRIMARY KEY (`fid`,`type`,`id`,`module`),
  KEY `type_id` (`type`,`id`),
  KEY `fid_count` (`fid`,`count`),
  KEY `fid_module` (`fid`,`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Track where a file is used.';

-- Data exporting was unselected.


-- Dumping structure for table apex.filter
DROP TABLE IF EXISTS `filter`;
CREATE TABLE IF NOT EXISTS `filter` (
  `format` varchar(255) NOT NULL COMMENT 'Foreign key: The filter_format.format to which this filter is assigned.',
  `module` varchar(64) NOT NULL DEFAULT '' COMMENT 'The origin module of the filter.',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT 'Name of the filter being referenced.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'Weight of filter within format.',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT 'Filter enabled status. (1 = enabled, 0 = disabled)',
  `settings` longblob COMMENT 'A serialized array of name value pairs that store the filter settings for the specific format.',
  PRIMARY KEY (`format`,`name`),
  KEY `list` (`weight`,`module`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Table that maps filters (HTML corrector) to text formats ...';

-- Data exporting was unselected.


-- Dumping structure for table apex.filter_format
DROP TABLE IF EXISTS `filter_format`;
CREATE TABLE IF NOT EXISTS `filter_format` (
  `format` varchar(255) NOT NULL COMMENT 'Primary Key: Unique machine name of the format.',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'Name of the text format (Filtered HTML).',
  `cache` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Flag to indicate whether format is cacheable. (1 = cacheable, 0 = not cacheable)',
  `status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'The status of the text format. (1 = enabled, 0 = disabled)',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'Weight of text format to use when listing.',
  PRIMARY KEY (`format`),
  UNIQUE KEY `name` (`name`),
  KEY `status_weight` (`status`,`weight`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores text formats: custom groupings of filters, such as...';

-- Data exporting was unselected.


-- Dumping structure for table apex.flood
DROP TABLE IF EXISTS `flood`;
CREATE TABLE IF NOT EXISTS `flood` (
  `fid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique flood event ID.',
  `event` varchar(64) NOT NULL DEFAULT '' COMMENT 'Name of event (e.g. contact).',
  `identifier` varchar(128) NOT NULL DEFAULT '' COMMENT 'Identifier of the visitor, such as an IP address or hostname.',
  `timestamp` int(11) NOT NULL DEFAULT '0' COMMENT 'Timestamp of the event.',
  `expiration` int(11) NOT NULL DEFAULT '0' COMMENT 'Expiration timestamp. Expired events are purged on cron run.',
  PRIMARY KEY (`fid`),
  KEY `allow` (`event`,`identifier`,`timestamp`),
  KEY `purge` (`expiration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Flood controls the threshold of events, such as the...';

-- Data exporting was unselected.


-- Dumping structure for table apex.headerimage
DROP TABLE IF EXISTS `headerimage`;
CREATE TABLE IF NOT EXISTS `headerimage` (
  `nid` int(10) unsigned NOT NULL DEFAULT '0',
  `block` varchar(32) NOT NULL DEFAULT '0',
  `weight` tinyint(4) NOT NULL DEFAULT '0',
  `conditions` text NOT NULL,
  PRIMARY KEY (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table apex.headerimage_block
DROP TABLE IF EXISTS `headerimage_block`;
CREATE TABLE IF NOT EXISTS `headerimage_block` (
  `delta` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`delta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table apex.history
DROP TABLE IF EXISTS `history`;
CREATE TABLE IF NOT EXISTS `history` (
  `uid` int(11) NOT NULL DEFAULT '0' COMMENT 'The users.uid that read the node nid.',
  `nid` int(11) NOT NULL DEFAULT '0' COMMENT 'The node.nid that was read.',
  `timestamp` int(11) NOT NULL DEFAULT '0' COMMENT 'The Unix timestamp at which the read occurred.',
  PRIMARY KEY (`uid`,`nid`),
  KEY `nid` (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='A record of which users have read which nodes.';

-- Data exporting was unselected.


-- Dumping structure for table apex.image_effects
DROP TABLE IF EXISTS `image_effects`;
CREATE TABLE IF NOT EXISTS `image_effects` (
  `ieid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The primary identifier for an image effect.',
  `isid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The image_styles.isid for an image style.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'The weight of the effect in the style.',
  `name` varchar(255) NOT NULL COMMENT 'The unique name of the effect to be executed.',
  `data` longblob NOT NULL COMMENT 'The configuration data for the effect.',
  PRIMARY KEY (`ieid`),
  KEY `isid` (`isid`),
  KEY `weight` (`weight`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores configuration options for image effects.';

-- Data exporting was unselected.


-- Dumping structure for table apex.image_styles
DROP TABLE IF EXISTS `image_styles`;
CREATE TABLE IF NOT EXISTS `image_styles` (
  `isid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The primary identifier for an image style.',
  `name` varchar(255) NOT NULL COMMENT 'The style machine name.',
  `label` varchar(255) NOT NULL DEFAULT '' COMMENT 'The style administrative name.',
  PRIMARY KEY (`isid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores configuration options for image styles.';

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_climate_average_temp_summary
DROP TABLE IF EXISTS `landpks_climate_average_temp_summary`;
CREATE TABLE IF NOT EXISTS `landpks_climate_average_temp_summary` (
  `ID` bigint(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` bigint(50) unsigned DEFAULT '0',
  `plot_id` bigint(50) unsigned DEFAULT '0',
  `record_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT '',
  `latitude` double DEFAULT '0',
  `longitude` double DEFAULT '0',
  `climate_avg_temp_jan` double DEFAULT '0',
  `climate_avg_temp_feb` double DEFAULT '0',
  `climate_avg_temp_mar` double DEFAULT '0',
  `climate_avg_temp_apr` double DEFAULT '0',
  `climate_avg_temp_may` double DEFAULT '0',
  `climate_avg_temp_jun` double DEFAULT '0',
  `climate_avg_temp_jul` double DEFAULT '0',
  `climate_avg_temp_aug` double DEFAULT '0',
  `climate_avg_temp_sep` double DEFAULT '0',
  `climate_avg_temp_oct` double DEFAULT '0',
  `climate_avg_temp_nov` double DEFAULT '0',
  `climate_avg_temp_dec` double DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_climate_max_temp_summary
DROP TABLE IF EXISTS `landpks_climate_max_temp_summary`;
CREATE TABLE IF NOT EXISTS `landpks_climate_max_temp_summary` (
  `ID` bigint(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` bigint(50) unsigned DEFAULT '0',
  `plot_id` bigint(50) unsigned DEFAULT '0',
  `record_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT '',
  `latitude` double DEFAULT '0',
  `longitude` double DEFAULT '0',
  `climate_max_temp_jan` double DEFAULT '0',
  `climate_max_temp_feb` double DEFAULT '0',
  `climate_max_temp_mar` double DEFAULT '0',
  `climate_max_temp_apr` double DEFAULT '0',
  `climate_max_temp_may` double DEFAULT '0',
  `climate_max_temp_jun` double DEFAULT '0',
  `climate_max_temp_jul` double DEFAULT '0',
  `climate_max_temp_aug` double DEFAULT '0',
  `climate_max_temp_sep` double DEFAULT '0',
  `climate_max_temp_oct` double DEFAULT '0',
  `climate_max_temp_nov` double DEFAULT '0',
  `climate_max_temp_dec` double DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_climate_min_temp_summary
DROP TABLE IF EXISTS `landpks_climate_min_temp_summary`;
CREATE TABLE IF NOT EXISTS `landpks_climate_min_temp_summary` (
  `ID` bigint(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` bigint(50) unsigned DEFAULT '0',
  `plot_id` bigint(50) unsigned DEFAULT '0',
  `record_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT '',
  `latitude` double DEFAULT '0',
  `longitude` double DEFAULT '0',
  `climate_min_temp_jan` double DEFAULT '0',
  `climate_min_temp_feb` double DEFAULT '0',
  `climate_min_temp_mar` double DEFAULT '0',
  `climate_min_temp_apr` double DEFAULT '0',
  `climate_min_temp_may` double DEFAULT '0',
  `climate_min_temp_jun` double DEFAULT '0',
  `climate_min_temp_jul` double DEFAULT '0',
  `climate_min_temp_aug` double DEFAULT '0',
  `climate_min_temp_sep` double DEFAULT '0',
  `climate_min_temp_oct` double DEFAULT '0',
  `climate_min_temp_nov` double DEFAULT '0',
  `climate_min_temp_dec` double DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_climate_precip_summary
DROP TABLE IF EXISTS `landpks_climate_precip_summary`;
CREATE TABLE IF NOT EXISTS `landpks_climate_precip_summary` (
  `ID` bigint(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` bigint(50) unsigned DEFAULT '0',
  `plot_id` bigint(50) unsigned DEFAULT '0',
  `record_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT '',
  `latitude` double DEFAULT '0',
  `longitude` double DEFAULT '0',
  `climate_precip_jan` double DEFAULT '0',
  `climate_precip_feb` double DEFAULT '0',
  `climate_precip_mar` double DEFAULT '0',
  `climate_precip_apr` double DEFAULT '0',
  `climate_precip_may` double DEFAULT '0',
  `climate_precip_jun` double DEFAULT '0',
  `climate_precip_jul` double DEFAULT '0',
  `climate_precip_aug` double DEFAULT '0',
  `climate_precip_sep` double DEFAULT '0',
  `climate_precip_oct` double DEFAULT '0',
  `climate_precip_nov` double DEFAULT '0',
  `climate_precip_dec` double DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_cereals_suitability_lookup
DROP TABLE IF EXISTS `landpks_gdal_cereals_suitability_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_cereals_suitability_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `cereals_suitability_class` varchar(30) COLLATE utf8_unicode_ci DEFAULT '',
  `cereals_suitability_si` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `cereals_suitability_label` varchar(15) COLLATE utf8_unicode_ci DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_data_country_level
DROP TABLE IF EXISTS `landpks_gdal_data_country_level`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_data_country_level` (
  `ID` int(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` int(50) unsigned DEFAULT '0',
  `plot_id` int(50) unsigned DEFAULT '0',
  `record_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT '',
  `latitude` double DEFAULT '0',
  `longitude` double DEFAULT '0',
  `country_code_data` varchar(5) COLLATE utf8_unicode_ci DEFAULT '',
  `country_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
  `slope_percentage` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `slope_reclassified` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `plane_curvature` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `profile_curvature` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `curvature` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `dem` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `aspect` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_data_global_level
DROP TABLE IF EXISTS `landpks_gdal_data_global_level`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_data_global_level` (
  `ID` int(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` int(50) DEFAULT '0',
  `plot_id` int(50) DEFAULT '0',
  `record_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `country_code_data` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_slate_weather_data` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_precipitation_data` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_gdd` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_aridity_index` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_kopgeiger` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_fao_lgp` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_modis_evapotrans` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_precip_novdecjan` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_precip_febmarapr` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_precip_mayjunjul` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_precip_augsepoct` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_1` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_2` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_3` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_4` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_5` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_6` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_7` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_8` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_9` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_10` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_11` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clim_wind_data_12` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_hwsd_data` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_depth_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_textclass_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_fert_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_workab_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_toxic_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_elevation` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_aspect` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_geolage` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_dem_global` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_dem_old` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_slope_global` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_landform_global` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_twi_global` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_topi_global` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `topog_israd_global` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_modis_2001` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_modis_2002` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_modis_2004` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_modis_2010` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_modis_2011` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_modis_2012` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_cult_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_irrcult_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_grass_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_protect_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landcover_agnprotect_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vegind_modis_evi_m` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vegind_modis_evi_sd` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vegind_modis_lai_m` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vegind_modis_lai_sd` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `manage_cerealsuit_low_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `manage_cerealsuit_hight_gaez` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pop_density` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `afsis_topog_dem` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `afsis_topog_twi` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `afsis_topog_sca` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_fao_lgp_lookup
DROP TABLE IF EXISTS `landpks_gdal_fao_lgp_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_fao_lgp_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `lgp_value` varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `label` varchar(20) COLLATE utf8_unicode_ci DEFAULT '',
  UNIQUE KEY `gdal_value` (`gdal_value`),
  KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_landcover_modis_lookup
DROP TABLE IF EXISTS `landpks_gdal_landcover_modis_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_landcover_modis_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `color` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `name` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
  `description` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `minimum` double DEFAULT '0',
  `maximum` double DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_landcover_protected_areas_lookup
DROP TABLE IF EXISTS `landpks_gdal_landcover_protected_areas_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_landcover_protected_areas_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `protected_area_value` varchar(30) COLLATE utf8_unicode_ci DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_landcover_protect_agri_lookup
DROP TABLE IF EXISTS `landpks_gdal_landcover_protect_agri_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_landcover_protect_agri_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `protected_area_agri_value` varchar(30) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_soil_depth_gaez_lookup
DROP TABLE IF EXISTS `landpks_gdal_soil_depth_gaez_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_soil_depth_gaez_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `depth_value` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_soil_fert_gaez_lookup
DROP TABLE IF EXISTS `landpks_gdal_soil_fert_gaez_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_soil_fert_gaez_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `fertility_value` varchar(40) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_soil_textclass_gaez_lookup
DROP TABLE IF EXISTS `landpks_gdal_soil_textclass_gaez_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_soil_textclass_gaez_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `texture_class_value` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_soil_toxic_gaez_lookup
DROP TABLE IF EXISTS `landpks_gdal_soil_toxic_gaez_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_soil_toxic_gaez_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `soil_toxic_value` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_soil_workab_gaez_lookup
DROP TABLE IF EXISTS `landpks_gdal_soil_workab_gaez_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_soil_workab_gaez_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `workability_value` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_gdal_worldkgeiger_lookup
DROP TABLE IF EXISTS `landpks_gdal_worldkgeiger_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_gdal_worldkgeiger_lookup` (
  `ID` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `gdal_value` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `count` int(10) unsigned NOT NULL DEFAULT '0',
  `desc` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  UNIQUE KEY `gdal_value` (`gdal_value`),
  UNIQUE KEY `desc` (`desc`),
  KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_input_data
DROP TABLE IF EXISTS `landpks_input_data`;
CREATE TABLE IF NOT EXISTS `landpks_input_data` (
  `ID` bigint(50) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recorder_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `test_plot` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_test_plot` tinyint(4) DEFAULT NULL,
  `organization` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` double DEFAULT '0',
  `longitude` double DEFAULT '0',
  `city` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `notes` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `modified_date` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `land_cover` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `grazed` varchar(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_grazed` tinyint(4) DEFAULT NULL,
  `grazing` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `flooding` varchar(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_flooding` tinyint(4) DEFAULT NULL,
  `slope` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `slope_shape` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bedrock_depth` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `stopped_digging_depth` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rock_fragment_for_soil_horizon_1` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rock_fragment_for_soil_horizon_2` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rock_fragment_for_soil_horizon_3` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rock_fragment_for_soil_horizon_4` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rock_fragment_for_soil_horizon_5` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rock_fragment_for_soil_horizon_6` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rock_fragment_for_soil_horizon_7` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color_for_soil_horizon_1` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color_for_soil_horizon_2` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color_for_soil_horizon_3` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color_for_soil_horizon_4` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color_for_soil_horizon_5` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color_for_soil_horizon_6` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color_for_soil_horizon_7` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `texture_for_soil_horizon_1` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `texture_for_soil_horizon_2` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `texture_for_soil_horizon_3` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `texture_for_soil_horizon_4` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `texture_for_soil_horizon_5` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `texture_for_soil_horizon_6` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `texture_for_soil_horizon_7` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `surface_cracking` varchar(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_surface_cracking` tinyint(4) DEFAULT NULL,
  `surface_salt` varchar(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_surface_salt` tinyint(4) DEFAULT NULL,
  `soil_pit_photo_url` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_samples_photo_url` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landscape_north_photo_url` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landscape_east_photo_url` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landscape_south_photo_url` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landscape_west_photo_url` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `insert_unix_time` bigint(20) DEFAULT NULL,
  `insert_normal_time` datetime DEFAULT NULL,
  `ip_address` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `deleted` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='LandPKS input data from mobile application to server';

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_map_input_files
DROP TABLE IF EXISTS `landpks_map_input_files`;
CREATE TABLE IF NOT EXISTS `landpks_map_input_files` (
  `ID` int(10) unsigned NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `dly_file_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_output_data
DROP TABLE IF EXISTS `landpks_output_data`;
CREATE TABLE IF NOT EXISTS `landpks_output_data` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `grass_productivity` double DEFAULT '0',
  `maize_productivity` double DEFAULT '0',
  `maize_erosion` double DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='LandPKS output data - Get from RUN APEX Model';

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_rosetta_awc_output_data
DROP TABLE IF EXISTS `landpks_rosetta_awc_output_data`;
CREATE TABLE IF NOT EXISTS `landpks_rosetta_awc_output_data` (
  `ID` int(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` int(50) DEFAULT '0',
  `plot_id` int(50) DEFAULT '0',
  `record_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `field_capacity_layer_1` double DEFAULT NULL,
  `field_capacity_layer_2` double DEFAULT NULL,
  `field_capacity_layer_3` double DEFAULT NULL,
  `field_capacity_layer_4` double DEFAULT NULL,
  `field_capacity_layer_5` double DEFAULT NULL,
  `field_capacity_layer_6` double DEFAULT NULL,
  `field_capacity_layer_7` double DEFAULT NULL,
  `wilting_point_layer_1` double DEFAULT NULL,
  `wilting_point_layer_2` double DEFAULT NULL,
  `wilting_point_layer_3` double DEFAULT NULL,
  `wilting_point_layer_4` double DEFAULT NULL,
  `wilting_point_layer_5` double DEFAULT NULL,
  `wilting_point_layer_6` double DEFAULT NULL,
  `wilting_point_layer_7` double DEFAULT NULL,
  `original_awc_layer_1` double DEFAULT NULL,
  `original_awc_layer_2` double DEFAULT NULL,
  `original_awc_layer_3` double DEFAULT NULL,
  `original_awc_layer_4` double DEFAULT NULL,
  `original_awc_layer_5` double DEFAULT NULL,
  `original_awc_layer_6` double DEFAULT NULL,
  `original_awc_layer_7` double DEFAULT NULL,
  `centimeter_awc_layer_1` double DEFAULT NULL,
  `centimeter_awc_layer_2` double DEFAULT NULL,
  `centimeter_awc_layer_3` double DEFAULT NULL,
  `centimeter_awc_layer_4` double DEFAULT NULL,
  `centimeter_awc_layer_5` double DEFAULT NULL,
  `centimeter_awc_layer_6` double DEFAULT NULL,
  `centimeter_awc_layer_7` double DEFAULT NULL,
  `soil_profile_awc` double DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.landpks_soil_texture_lookup
DROP TABLE IF EXISTS `landpks_soil_texture_lookup`;
CREATE TABLE IF NOT EXISTS `landpks_soil_texture_lookup` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `texture` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `sand` double NOT NULL DEFAULT '0',
  `silt` double NOT NULL DEFAULT '0',
  `clay` double NOT NULL DEFAULT '0',
  `bulk_density` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.lanpks_apex_output_data
DROP TABLE IF EXISTS `lanpks_apex_output_data`;
CREATE TABLE IF NOT EXISTS `lanpks_apex_output_data` (
  `ID` bigint(50) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` bigint(50) unsigned NOT NULL DEFAULT '0',
  `plot_id` bigint(50) unsigned NOT NULL DEFAULT '0',
  `record_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'unknown',
  `apex_output_y_maize` double NOT NULL DEFAULT '0',
  `apex_output_yldg_maize` double NOT NULL DEFAULT '0',
  `apex_output_biom_meize` double NOT NULL DEFAULT '0',
  `apex_output_y_glass` double NOT NULL DEFAULT '0',
  `apex_output_yldg_glass` double NOT NULL DEFAULT '0',
  `apex_output_biom_glass` double NOT NULL DEFAULT '0',
  `maize_productivity` double NOT NULL DEFAULT '0',
  `maize_erosion` double NOT NULL DEFAULT '0',
  `glass_productivity` double NOT NULL DEFAULT '0',
  `glass_erosion` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.menu_custom
DROP TABLE IF EXISTS `menu_custom`;
CREATE TABLE IF NOT EXISTS `menu_custom` (
  `menu_name` varchar(32) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique key for menu. This is used as a block delta so length is 32.',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT 'Menu title; displayed at top of block.',
  `description` text COMMENT 'Menu description.',
  PRIMARY KEY (`menu_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Holds definitions for top-level custom menus (for example...';

-- Data exporting was unselected.


-- Dumping structure for table apex.menu_links
DROP TABLE IF EXISTS `menu_links`;
CREATE TABLE IF NOT EXISTS `menu_links` (
  `menu_name` varchar(32) NOT NULL DEFAULT '' COMMENT 'The menu name. All links with the same menu name (such as ’navigation’) are part of the same menu.',
  `mlid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The menu link ID (mlid) is the integer primary key.',
  `plid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The parent link ID (plid) is the mlid of the link above in the hierarchy, or zero if the link is at the top level in its menu.',
  `link_path` varchar(255) NOT NULL DEFAULT '' COMMENT 'The Drupal path or external path this link points to.',
  `router_path` varchar(255) NOT NULL DEFAULT '' COMMENT 'For links corresponding to a Drupal path (external = 0), this connects the link to a menu_router.path for joins.',
  `link_title` varchar(255) NOT NULL DEFAULT '' COMMENT 'The text displayed for the link, which may be modified by a title callback stored in menu_router.',
  `options` blob COMMENT 'A serialized array of options to be passed to the url() or l() function, such as a query string or HTML attributes.',
  `module` varchar(255) NOT NULL DEFAULT 'system' COMMENT 'The name of the module that generated this link.',
  `hidden` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag for whether the link should be rendered in menus. (1 = a disabled menu item that may be shown on admin screens, -1 = a menu callback, 0 = a normal, visible link)',
  `external` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate if the link points to a full URL starting with a protocol, like http:// (1 = external, 0 = internal).',
  `has_children` smallint(6) NOT NULL DEFAULT '0' COMMENT 'Flag indicating whether any links have this link as a parent (1 = children exist, 0 = no children).',
  `expanded` smallint(6) NOT NULL DEFAULT '0' COMMENT 'Flag for whether this link should be rendered as expanded in menus - expanded links always have their child links displayed, instead of only when the link is in the active trail (1 = expanded, 0 = not expanded)',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'Link weight among links in the same menu at the same depth.',
  `depth` smallint(6) NOT NULL DEFAULT '0' COMMENT 'The depth relative to the top level. A link with plid == 0 will have depth == 1.',
  `customized` smallint(6) NOT NULL DEFAULT '0' COMMENT 'A flag to indicate that the user has manually created or edited the link (1 = customized, 0 = not customized).',
  `p1` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The first mlid in the materialized path. If N = depth, then pN must equal the mlid. If depth > 1 then p(N-1) must equal the plid. All pX where X > depth must equal zero. The columns p1 .. p9 are also called the parents.',
  `p2` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The second mlid in the materialized path. See p1.',
  `p3` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The third mlid in the materialized path. See p1.',
  `p4` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The fourth mlid in the materialized path. See p1.',
  `p5` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The fifth mlid in the materialized path. See p1.',
  `p6` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The sixth mlid in the materialized path. See p1.',
  `p7` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The seventh mlid in the materialized path. See p1.',
  `p8` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The eighth mlid in the materialized path. See p1.',
  `p9` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The ninth mlid in the materialized path. See p1.',
  `updated` smallint(6) NOT NULL DEFAULT '0' COMMENT 'Flag that indicates that this link was generated during the update from Drupal 5.',
  PRIMARY KEY (`mlid`),
  KEY `path_menu` (`link_path`(128),`menu_name`),
  KEY `menu_plid_expand_child` (`menu_name`,`plid`,`expanded`,`has_children`),
  KEY `menu_parents` (`menu_name`,`p1`,`p2`,`p3`,`p4`,`p5`,`p6`,`p7`,`p8`,`p9`),
  KEY `router_path` (`router_path`(128))
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Contains the individual links within a menu.';

-- Data exporting was unselected.


-- Dumping structure for table apex.menu_router
DROP TABLE IF EXISTS `menu_router`;
CREATE TABLE IF NOT EXISTS `menu_router` (
  `path` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: the Drupal path this entry describes',
  `load_functions` blob NOT NULL COMMENT 'A serialized array of function names (like node_load) to be called to load an object corresponding to a part of the current path.',
  `to_arg_functions` blob NOT NULL COMMENT 'A serialized array of function names (like user_uid_optional_to_arg) to be called to replace a part of the router path with another string.',
  `access_callback` varchar(255) NOT NULL DEFAULT '' COMMENT 'The callback which determines the access to this router path. Defaults to user_access.',
  `access_arguments` blob COMMENT 'A serialized array of arguments for the access callback.',
  `page_callback` varchar(255) NOT NULL DEFAULT '' COMMENT 'The name of the function that renders the page.',
  `page_arguments` blob COMMENT 'A serialized array of arguments for the page callback.',
  `delivery_callback` varchar(255) NOT NULL DEFAULT '' COMMENT 'The name of the function that sends the result of the page_callback function to the browser.',
  `fit` int(11) NOT NULL DEFAULT '0' COMMENT 'A numeric representation of how specific the path is.',
  `number_parts` smallint(6) NOT NULL DEFAULT '0' COMMENT 'Number of parts in this router path.',
  `context` int(11) NOT NULL DEFAULT '0' COMMENT 'Only for local tasks (tabs) - the context of a local task to control its placement.',
  `tab_parent` varchar(255) NOT NULL DEFAULT '' COMMENT 'Only for local tasks (tabs) - the router path of the parent page (which may also be a local task).',
  `tab_root` varchar(255) NOT NULL DEFAULT '' COMMENT 'Router path of the closest non-tab parent page. For pages that are not local tasks, this will be the same as the path.',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT 'The title for the current page, or the title for the tab if this is a local task.',
  `title_callback` varchar(255) NOT NULL DEFAULT '' COMMENT 'A function which will alter the title. Defaults to t()',
  `title_arguments` varchar(255) NOT NULL DEFAULT '' COMMENT 'A serialized array of arguments for the title callback. If empty, the title will be used as the sole argument for the title callback.',
  `theme_callback` varchar(255) NOT NULL DEFAULT '' COMMENT 'A function which returns the name of the theme that will be used to render this page. If left empty, the default theme will be used.',
  `theme_arguments` varchar(255) NOT NULL DEFAULT '' COMMENT 'A serialized array of arguments for the theme callback.',
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Numeric representation of the type of the menu item, like MENU_LOCAL_TASK.',
  `description` text NOT NULL COMMENT 'A description of this item.',
  `position` varchar(255) NOT NULL DEFAULT '' COMMENT 'The position of the block (left or right) on the system administration page for this item.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'Weight of the element. Lighter weights are higher up, heavier weights go down.',
  `include_file` mediumtext COMMENT 'The file to include for this element, usually the page callback function lives in this file.',
  PRIMARY KEY (`path`),
  KEY `fit` (`fit`),
  KEY `tab_parent` (`tab_parent`(64),`weight`,`title`),
  KEY `tab_root_weight_title` (`tab_root`(64),`weight`,`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Maps paths to various callbacks (access, page and title)';

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_input_plots
DROP TABLE IF EXISTS `new_landpks_input_plots`;
CREATE TABLE IF NOT EXISTS `new_landpks_input_plots` (
  `ID` int(50) unsigned NOT NULL AUTO_INCREMENT,
  `plot_id` varchar(500) COLLATE utf8_unicode_ci DEFAULT '0',
  `name` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recorder_name` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `organization` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` double DEFAULT '0',
  `longitude` double DEFAULT '0',
  `city` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `modified_date` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landpks_landcover_category_id` tinyint(4) DEFAULT '0',
  `grazed` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_grazed` tinyint(4) DEFAULT NULL,
  `flooding` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_flooding` tinyint(4) DEFAULT NULL,
  `landpks_slope_category_id` tinyint(4) DEFAULT '0',
  `slope_measured` double DEFAULT '0',
  `landpks_slope_shape_category_id` tinyint(4) DEFAULT '0',
  `surface_cracking` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_surface_cracking` tinyint(4) DEFAULT NULL,
  `surface_salt` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `boolean_surface_salt` tinyint(4) DEFAULT NULL,
  `landscape_north_photo_url` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landscape_east_photo_url` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landscape_south_photo_url` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landscape_west_photo_url` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_pit_photo_url` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soil_samples_photo_url` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `insert_unix_time` bigint(20) DEFAULT NULL,
  `insert_normal_time` datetime DEFAULT NULL,
  `ip_address` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_landcover_categories
DROP TABLE IF EXISTS `new_landpks_landcover_categories`;
CREATE TABLE IF NOT EXISTS `new_landpks_landcover_categories` (
  `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `landcover_value` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_slope_categories
DROP TABLE IF EXISTS `new_landpks_slope_categories`;
CREATE TABLE IF NOT EXISTS `new_landpks_slope_categories` (
  `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `slope_value` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_slope_shape_categories
DROP TABLE IF EXISTS `new_landpks_slope_shape_categories`;
CREATE TABLE IF NOT EXISTS `new_landpks_slope_shape_categories` (
  `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `slope_shape_value` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_soil_horizons
DROP TABLE IF EXISTS `new_landpks_soil_horizons`;
CREATE TABLE IF NOT EXISTS `new_landpks_soil_horizons` (
  `ID` int(50) unsigned NOT NULL AUTO_INCREMENT,
  `int_plot_id` int(50) DEFAULT '0',
  `plot_id` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `landpks_soil_horizon_depth_id` tinyint(4) DEFAULT '0',
  `landpks_soil_texture_category_id` tinyint(4) DEFAULT '0',
  `landpks_soil_rock_fragment_category_id` tinyint(4) DEFAULT '0',
  `color` int(11) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_soil_horizon_depths
DROP TABLE IF EXISTS `new_landpks_soil_horizon_depths`;
CREATE TABLE IF NOT EXISTS `new_landpks_soil_horizon_depths` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `soil_horizon_depth_value` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_soil_rock_fragment_categories
DROP TABLE IF EXISTS `new_landpks_soil_rock_fragment_categories`;
CREATE TABLE IF NOT EXISTS `new_landpks_soil_rock_fragment_categories` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `soil_rock_fragment_value` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.new_landpks_soil_texture_categories
DROP TABLE IF EXISTS `new_landpks_soil_texture_categories`;
CREATE TABLE IF NOT EXISTS `new_landpks_soil_texture_categories` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `soil_texture_value` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.


-- Dumping structure for table apex.nextag_items
DROP TABLE IF EXISTS `nextag_items`;
CREATE TABLE IF NOT EXISTS `nextag_items` (
  `itemid` mediumint(9) NOT NULL COMMENT 'TODO: please describe this field!',
  `type` varchar(32) NOT NULL COMMENT 'TODO: please describe this field!',
  `tags` text COMMENT 'TODO: please describe this field!',
  KEY `itemid` (`itemid`),
  KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.nextag_metrics
DROP TABLE IF EXISTS `nextag_metrics`;
CREATE TABLE IF NOT EXISTS `nextag_metrics` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `tagid` int(11) NOT NULL COMMENT 'TODO: please describe this field!',
  `type` varchar(32) NOT NULL COMMENT 'TODO: please describe this field!',
  `groupid` mediumint(9) DEFAULT NULL COMMENT 'TODO: please describe this field!',
  `roleid` mediumint(9) DEFAULT NULL COMMENT 'TODO: please describe this field!',
  `metric` smallint(6) NOT NULL COMMENT 'TODO: please describe this field!',
  `last_updated` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`),
  KEY `tagid` (`tagid`),
  KEY `type` (`type`),
  KEY `uid` (`roleid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.nextag_words
DROP TABLE IF EXISTS `nextag_words`;
CREATE TABLE IF NOT EXISTS `nextag_words` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'TODO: please describe this field!',
  `tagword` varchar(32) NOT NULL COMMENT 'TODO: please describe this field!',
  `displayword` varchar(32) DEFAULT NULL COMMENT 'TODO: please describe this field!',
  `metric` smallint(6) NOT NULL DEFAULT '1' COMMENT 'TODO: please describe this field!',
  `last_updated` int(11) NOT NULL DEFAULT '0' COMMENT 'TODO: please describe this field!',
  PRIMARY KEY (`id`),
  KEY `tagword` (`tagword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='TODO: please describe this table!';

-- Data exporting was unselected.


-- Dumping structure for table apex.node
DROP TABLE IF EXISTS `node`;
CREATE TABLE IF NOT EXISTS `node` (
  `nid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The primary identifier for a node.',
  `vid` int(10) unsigned DEFAULT NULL COMMENT 'The current node_revision.vid version identifier.',
  `type` varchar(32) NOT NULL DEFAULT '' COMMENT 'The node_type.type of this node.',
  `language` varchar(12) NOT NULL DEFAULT '' COMMENT 'The languages.language of this node.',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT 'The title of this node, always treated as non-markup plain text.',
  `uid` int(11) NOT NULL DEFAULT '0' COMMENT 'The users.uid that owns this node; initially, this is the user that created it.',
  `status` int(11) NOT NULL DEFAULT '1' COMMENT 'Boolean indicating whether the node is published (visible to non-administrators).',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'The Unix timestamp when the node was created.',
  `changed` int(11) NOT NULL DEFAULT '0' COMMENT 'The Unix timestamp when the node was most recently saved.',
  `comment` int(11) NOT NULL DEFAULT '0' COMMENT 'Whether comments are allowed on this node: 0 = no, 1 = closed (read only), 2 = open (read/write).',
  `promote` int(11) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether the node should be displayed on the front page.',
  `sticky` int(11) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether the node should be displayed at the top of lists in which it appears.',
  `tnid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The translation set id for this node, which equals the node id of the source post in each set.',
  `translate` int(11) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this translation page needs to be updated.',
  PRIMARY KEY (`nid`),
  UNIQUE KEY `vid` (`vid`),
  KEY `node_changed` (`changed`),
  KEY `node_created` (`created`),
  KEY `node_frontpage` (`promote`,`status`,`sticky`,`created`),
  KEY `node_status_type` (`status`,`type`,`nid`),
  KEY `node_title_type` (`title`,`type`(4)),
  KEY `node_type` (`type`(4)),
  KEY `uid` (`uid`),
  KEY `tnid` (`tnid`),
  KEY `translate` (`translate`),
  KEY `language` (`language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='The base table for nodes.';

-- Data exporting was unselected.


-- Dumping structure for table apex.node_access
DROP TABLE IF EXISTS `node_access`;
CREATE TABLE IF NOT EXISTS `node_access` (
  `nid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The node.nid this record affects.',
  `gid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The grant ID a user must possess in the specified realm to gain this row’s privileges on the node.',
  `realm` varchar(255) NOT NULL DEFAULT '' COMMENT 'The realm in which the user must possess the grant ID. Each node access node can define one or more realms.',
  `grant_view` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether a user with the realm/grant pair can view this node.',
  `grant_update` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether a user with the realm/grant pair can edit this node.',
  `grant_delete` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether a user with the realm/grant pair can delete this node.',
  PRIMARY KEY (`nid`,`gid`,`realm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Identifies which realm/grant pairs a user must possess in...';

-- Data exporting was unselected.


-- Dumping structure for table apex.node_comment_statistics
DROP TABLE IF EXISTS `node_comment_statistics`;
CREATE TABLE IF NOT EXISTS `node_comment_statistics` (
  `nid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The node.nid for which the statistics are compiled.',
  `cid` int(11) NOT NULL DEFAULT '0' COMMENT 'The comment.cid of the last comment.',
  `last_comment_timestamp` int(11) NOT NULL DEFAULT '0' COMMENT 'The Unix timestamp of the last comment that was posted within this node, from comment.changed.',
  `last_comment_name` varchar(60) DEFAULT NULL COMMENT 'The name of the latest author to post a comment on this node, from comment.name.',
  `last_comment_uid` int(11) NOT NULL DEFAULT '0' COMMENT 'The user ID of the latest author to post a comment on this node, from comment.uid.',
  `comment_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The total number of comments on this node.',
  PRIMARY KEY (`nid`),
  KEY `node_comment_timestamp` (`last_comment_timestamp`),
  KEY `comment_count` (`comment_count`),
  KEY `last_comment_uid` (`last_comment_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Maintains statistics of node and comments posts to show ...';

-- Data exporting was unselected.


-- Dumping structure for table apex.node_revision
DROP TABLE IF EXISTS `node_revision`;
CREATE TABLE IF NOT EXISTS `node_revision` (
  `nid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The node this version belongs to.',
  `vid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The primary identifier for this version.',
  `uid` int(11) NOT NULL DEFAULT '0' COMMENT 'The users.uid that created this version.',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT 'The title of this version.',
  `log` longtext NOT NULL COMMENT 'The log entry explaining the changes in this version.',
  `timestamp` int(11) NOT NULL DEFAULT '0' COMMENT 'A Unix timestamp indicating when this version was created.',
  `status` int(11) NOT NULL DEFAULT '1' COMMENT 'Boolean indicating whether the node (at the time of this revision) is published (visible to non-administrators).',
  `comment` int(11) NOT NULL DEFAULT '0' COMMENT 'Whether comments are allowed on this node (at the time of this revision): 0 = no, 1 = closed (read only), 2 = open (read/write).',
  `promote` int(11) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether the node (at the time of this revision) should be displayed on the front page.',
  `sticky` int(11) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether the node (at the time of this revision) should be displayed at the top of lists in which it appears.',
  PRIMARY KEY (`vid`),
  KEY `nid` (`nid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores information about each saved version of a node.';

-- Data exporting was unselected.


-- Dumping structure for table apex.node_type
DROP TABLE IF EXISTS `node_type`;
CREATE TABLE IF NOT EXISTS `node_type` (
  `type` varchar(32) NOT NULL COMMENT 'The machine-readable name of this type.',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'The human-readable name of this type.',
  `base` varchar(255) NOT NULL COMMENT 'The base string used to construct callbacks corresponding to this node type.',
  `module` varchar(255) NOT NULL COMMENT 'The module defining this node type.',
  `description` mediumtext NOT NULL COMMENT 'A brief description of this type.',
  `help` mediumtext NOT NULL COMMENT 'Help information shown to the user when creating a node of this type.',
  `has_title` tinyint(3) unsigned NOT NULL COMMENT 'Boolean indicating whether this type uses the node.title field.',
  `title_label` varchar(255) NOT NULL DEFAULT '' COMMENT 'The label displayed for the title field on the edit form.',
  `custom` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this type is defined by a module (FALSE) or by a user via Add content type (TRUE).',
  `modified` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether this type has been modified by an administrator; currently not used in any way.',
  `locked` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether the administrator can change the machine name of this type.',
  `disabled` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'A boolean indicating whether the node type is disabled.',
  `orig_type` varchar(255) NOT NULL DEFAULT '' COMMENT 'The original machine-readable name of this node type. This may be different from the current type name if the locked field is 0.',
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores information about all defined node types.';

-- Data exporting was unselected.


-- Dumping structure for table apex.protected_pages
DROP TABLE IF EXISTS `protected_pages`;
CREATE TABLE IF NOT EXISTS `protected_pages` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The primary key always unique.',
  `password` varchar(128) NOT NULL COMMENT 'The password of the protected page.',
  `path` varchar(255) NOT NULL COMMENT 'The path of the protected page.',
  PRIMARY KEY (`pid`),
  KEY `path` (`path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table apex.queue
DROP TABLE IF EXISTS `queue`;
CREATE TABLE IF NOT EXISTS `queue` (
  `item_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique item ID.',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'The queue name.',
  `data` longblob COMMENT 'The arbitrary data for the item.',
  `expire` int(11) NOT NULL DEFAULT '0' COMMENT 'Timestamp when the claim lease expires on the item.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'Timestamp when the item was created.',
  PRIMARY KEY (`item_id`),
  KEY `name_created` (`name`,`created`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores items in queues.';

-- Data exporting was unselected.


-- Dumping structure for table apex.rdf_mapping
DROP TABLE IF EXISTS `rdf_mapping`;
CREATE TABLE IF NOT EXISTS `rdf_mapping` (
  `type` varchar(128) NOT NULL COMMENT 'The name of the entity type a mapping applies to (node, user, comment, etc.).',
  `bundle` varchar(128) NOT NULL COMMENT 'The name of the bundle a mapping applies to.',
  `mapping` longblob COMMENT 'The serialized mapping of the bundle type and fields to RDF terms.',
  PRIMARY KEY (`type`,`bundle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores custom RDF mappings for user defined content types...';

-- Data exporting was unselected.


-- Dumping structure for table apex.registry
DROP TABLE IF EXISTS `registry`;
CREATE TABLE IF NOT EXISTS `registry` (
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'The name of the function, class, or interface.',
  `type` varchar(9) NOT NULL DEFAULT '' COMMENT 'Either function or class or interface.',
  `filename` varchar(255) NOT NULL COMMENT 'Name of the file.',
  `module` varchar(255) NOT NULL DEFAULT '' COMMENT 'Name of the module the file belongs to.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'The order in which this module’s hooks should be invoked relative to other modules. Equal-weighted modules are ordered by name.',
  PRIMARY KEY (`name`,`type`),
  KEY `hook` (`type`,`weight`,`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Each record is a function, class, or interface name and...';

-- Data exporting was unselected.


-- Dumping structure for table apex.registry_file
DROP TABLE IF EXISTS `registry_file`;
CREATE TABLE IF NOT EXISTS `registry_file` (
  `filename` varchar(255) NOT NULL COMMENT 'Path to the file.',
  `hash` varchar(64) NOT NULL COMMENT 'sha-256 hash of the file’s contents when last parsed.',
  PRIMARY KEY (`filename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Files parsed to build the registry.';

-- Data exporting was unselected.


-- Dumping structure for table apex.rhm_input_data
DROP TABLE IF EXISTS `rhm_input_data`;
CREATE TABLE IF NOT EXISTS `rhm_input_data` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` bigint(50) unsigned NOT NULL DEFAULT '0',
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `recorder_name` varchar(150) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `transect` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dominant_woody_species` varchar(400) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dominant_nonwoody_species` varchar(400) COLLATE utf8_unicode_ci DEFAULT NULL,
  `species_of_interest_1` varchar(400) COLLATE utf8_unicode_ci DEFAULT NULL,
  `species_of_interest_2` varchar(400) COLLATE utf8_unicode_ci DEFAULT NULL,
  `segment` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `canopy_height` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `canopy_gap` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `basal_gap` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `species_1_density` int(11) DEFAULT '0',
  `species_2_density` int(11) DEFAULT '0',
  `species_of_interest_1_count` int(11) DEFAULT '0',
  `species_of_interest_2_count` int(11) DEFAULT '0',
  `species_list` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `stick_segment_0` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `stick_segment_1` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `stick_segment_2` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `stick_segment_3` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `stick_segment_4` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bare_total` int(11) DEFAULT '0',
  `trees_total` int(11) DEFAULT '0',
  `shrubs_total` int(11) DEFAULT '0',
  `sub_shrubs_total` int(11) unsigned DEFAULT '0',
  `perennial_grasses_total` int(11) DEFAULT '0',
  `annuals_total` int(11) DEFAULT '0',
  `herb_litter_total` int(11) DEFAULT '0',
  `wood_litter_total` int(11) DEFAULT '0',
  `rock_total` int(11) DEFAULT '0',
  `insert_unix_time` double DEFAULT '0',
  `insert_normal_time` varchar(50) COLLATE utf8_unicode_ci DEFAULT '0000-00-00 00:00:00',
  `ip_address` varchar(20) COLLATE utf8_unicode_ci DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='RHM Project Input Data';

-- Data exporting was unselected.


-- Dumping structure for table apex.rhm_ouput_summary_data
DROP TABLE IF EXISTS `rhm_ouput_summary_data`;
CREATE TABLE IF NOT EXISTS `rhm_ouput_summary_data` (
  `ID` int(50) NOT NULL AUTO_INCREMENT,
  `record_id` int(50) NOT NULL DEFAULT '0',
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  `total_record_consider` int(11) DEFAULT '0',
  `bare_ground_1_percent` double DEFAULT '0',
  `veg_cover_percent` double DEFAULT '0',
  `bare_ground_2_percent` double DEFAULT '0',
  `perennial_grass_percent` double DEFAULT '0',
  `tree_percent` double DEFAULT '0',
  `shrub_percent` double DEFAULT '0',
  `sub_shrub_percent` double DEFAULT '0',
  `annual_percent` double DEFAULT '0',
  `herb_litter_percent` double DEFAULT '0',
  `wood_litter_percent` double DEFAULT '0',
  `rock_percent` double DEFAULT '0',
  `canopy_gap_percent` double DEFAULT '0',
  `basal_gap_percent` double DEFAULT '0',
  `species_1_density` double DEFAULT '0',
  `species_2_density` double DEFAULT '0',
  `height_class_10cm` double DEFAULT '0',
  `height_class_10cm_50cm` double DEFAULT '0',
  `height_class_50cm_1m` double DEFAULT '0',
  `height_class_1m_2m` double DEFAULT '0',
  `height_class_2m_3m` double DEFAULT '0',
  `height_class_3m` double DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Sumary Output Data';

-- Data exporting was unselected.


-- Dumping structure for table apex.role
DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `rid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique role ID.',
  `name` varchar(64) NOT NULL DEFAULT '' COMMENT 'Unique role name.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'The weight of this role in listings and the user interface.',
  PRIMARY KEY (`rid`),
  UNIQUE KEY `name` (`name`),
  KEY `name_weight` (`name`,`weight`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores user roles.';

-- Data exporting was unselected.


-- Dumping structure for table apex.role_permission
DROP TABLE IF EXISTS `role_permission`;
CREATE TABLE IF NOT EXISTS `role_permission` (
  `rid` int(10) unsigned NOT NULL COMMENT 'Foreign Key: role.rid.',
  `permission` varchar(128) NOT NULL DEFAULT '' COMMENT 'A single permission granted to the role identified by rid.',
  `module` varchar(255) NOT NULL DEFAULT '' COMMENT 'The module declaring the permission.',
  PRIMARY KEY (`rid`,`permission`),
  KEY `permission` (`permission`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores the permissions assigned to user roles.';

-- Data exporting was unselected.


-- Dumping structure for table apex.search_dataset
DROP TABLE IF EXISTS `search_dataset`;
CREATE TABLE IF NOT EXISTS `search_dataset` (
  `sid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Search item ID, e.g. node ID for nodes.',
  `type` varchar(16) NOT NULL COMMENT 'Type of item, e.g. node.',
  `data` longtext NOT NULL COMMENT 'List of space-separated words from the item.',
  `reindex` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Set to force node reindexing.',
  PRIMARY KEY (`sid`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores items that will be searched.';

-- Data exporting was unselected.


-- Dumping structure for table apex.search_index
DROP TABLE IF EXISTS `search_index`;
CREATE TABLE IF NOT EXISTS `search_index` (
  `word` varchar(50) NOT NULL DEFAULT '' COMMENT 'The search_total.word that is associated with the search item.',
  `sid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The search_dataset.sid of the searchable item to which the word belongs.',
  `type` varchar(16) NOT NULL COMMENT 'The search_dataset.type of the searchable item to which the word belongs.',
  `score` float DEFAULT NULL COMMENT 'The numeric score of the word, higher being more important.',
  PRIMARY KEY (`word`,`sid`,`type`),
  KEY `sid_type` (`sid`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores the search index, associating words, items and...';

-- Data exporting was unselected.


-- Dumping structure for table apex.search_node_links
DROP TABLE IF EXISTS `search_node_links`;
CREATE TABLE IF NOT EXISTS `search_node_links` (
  `sid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The search_dataset.sid of the searchable item containing the link to the node.',
  `type` varchar(16) NOT NULL DEFAULT '' COMMENT 'The search_dataset.type of the searchable item containing the link to the node.',
  `nid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The node.nid that this item links to.',
  `caption` longtext COMMENT 'The text used to link to the node.nid.',
  PRIMARY KEY (`sid`,`type`,`nid`),
  KEY `nid` (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores items (like nodes) that link to other nodes, used...';

-- Data exporting was unselected.


-- Dumping structure for table apex.search_total
DROP TABLE IF EXISTS `search_total`;
CREATE TABLE IF NOT EXISTS `search_total` (
  `word` varchar(50) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique word in the search index.',
  `count` float DEFAULT NULL COMMENT 'The count of the word in the index using Zipf’s law to equalize the probability distribution.',
  PRIMARY KEY (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores search totals for words.';

-- Data exporting was unselected.


-- Dumping structure for table apex.semaphore
DROP TABLE IF EXISTS `semaphore`;
CREATE TABLE IF NOT EXISTS `semaphore` (
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'Primary Key: Unique name.',
  `value` varchar(255) NOT NULL DEFAULT '' COMMENT 'A value for the semaphore.',
  `expire` double NOT NULL COMMENT 'A Unix timestamp with microseconds indicating when the semaphore should expire.',
  PRIMARY KEY (`name`),
  KEY `value` (`value`),
  KEY `expire` (`expire`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Table for holding semaphores, locks, flags, etc. that...';

-- Data exporting was unselected.


-- Dumping structure for table apex.sequences
DROP TABLE IF EXISTS `sequences`;
CREATE TABLE IF NOT EXISTS `sequences` (
  `value` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The value of the sequence.',
  PRIMARY KEY (`value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores IDs.';

-- Data exporting was unselected.


-- Dumping structure for table apex.sessions
DROP TABLE IF EXISTS `sessions`;
CREATE TABLE IF NOT EXISTS `sessions` (
  `uid` int(10) unsigned NOT NULL COMMENT 'The users.uid corresponding to a session, or 0 for anonymous user.',
  `sid` varchar(128) NOT NULL COMMENT 'A session ID. The value is generated by Drupal’s session handlers.',
  `ssid` varchar(128) NOT NULL DEFAULT '' COMMENT 'Secure session ID. The value is generated by Drupal’s session handlers.',
  `hostname` varchar(128) NOT NULL DEFAULT '' COMMENT 'The IP address that last used this session ID (sid).',
  `timestamp` int(11) NOT NULL DEFAULT '0' COMMENT 'The Unix timestamp when this session last requested a page. Old records are purged by PHP automatically.',
  `cache` int(11) NOT NULL DEFAULT '0' COMMENT 'The time of this user’s last post. This is used when the site has specified a minimum_cache_lifetime. See cache_get().',
  `session` longblob COMMENT 'The serialized contents of $_SESSION, an array of name/value pairs that persists across page requests by this session ID. Drupal loads $_SESSION from here at the start of each request and saves it at the end.',
  PRIMARY KEY (`sid`,`ssid`),
  KEY `timestamp` (`timestamp`),
  KEY `uid` (`uid`),
  KEY `ssid` (`ssid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Drupal’s session handlers read and write into the...';

-- Data exporting was unselected.


-- Dumping structure for table apex.shortcut_set
DROP TABLE IF EXISTS `shortcut_set`;
CREATE TABLE IF NOT EXISTS `shortcut_set` (
  `set_name` varchar(32) NOT NULL DEFAULT '' COMMENT 'Primary Key: The menu_links.menu_name under which the set’s links are stored.',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT 'The title of the set.',
  PRIMARY KEY (`set_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores information about sets of shortcuts links.';

-- Data exporting was unselected.


-- Dumping structure for table apex.shortcut_set_users
DROP TABLE IF EXISTS `shortcut_set_users`;
CREATE TABLE IF NOT EXISTS `shortcut_set_users` (
  `uid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The users.uid for this set.',
  `set_name` varchar(32) NOT NULL DEFAULT '' COMMENT 'The shortcut_set.set_name that will be displayed for this user.',
  PRIMARY KEY (`uid`),
  KEY `set_name` (`set_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Maps users to shortcut sets.';

-- Data exporting was unselected.


-- Dumping structure for table apex.system
DROP TABLE IF EXISTS `system`;
CREATE TABLE IF NOT EXISTS `system` (
  `filename` varchar(255) NOT NULL DEFAULT '' COMMENT 'The path of the primary file for this item, relative to the Drupal root; e.g. modules/node/node.module.',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'The name of the item; e.g. node.',
  `type` varchar(12) NOT NULL DEFAULT '' COMMENT 'The type of the item, either module, theme, or theme_engine.',
  `owner` varchar(255) NOT NULL DEFAULT '' COMMENT 'A theme’s ’parent’ . Can be either a theme or an engine.',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether or not this item is enabled.',
  `bootstrap` int(11) NOT NULL DEFAULT '0' COMMENT 'Boolean indicating whether this module is loaded during Drupal’s early bootstrapping phase (e.g. even before the page cache is consulted).',
  `schema_version` smallint(6) NOT NULL DEFAULT '-1' COMMENT 'The module’s database schema version number. -1 if the module is not installed (its tables do not exist); 0 or the largest N of the module’s hook_update_N() function that has either been run or existed when the module was first installed.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'The order in which this module’s hooks should be invoked relative to other modules. Equal-weighted modules are ordered by name.',
  `info` blob COMMENT 'A serialized array containing information from the module’s .info file; keys can include name, description, package, version, core, dependencies, and php.',
  PRIMARY KEY (`filename`),
  KEY `system_list` (`status`,`bootstrap`,`type`,`weight`,`name`),
  KEY `type_name` (`type`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='A list of all modules, themes, and theme engines that are...';

-- Data exporting was unselected.


-- Dumping structure for table apex.taxonomy_index
DROP TABLE IF EXISTS `taxonomy_index`;
CREATE TABLE IF NOT EXISTS `taxonomy_index` (
  `nid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The node.nid this record tracks.',
  `tid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The term ID.',
  `sticky` tinyint(4) DEFAULT '0' COMMENT 'Boolean indicating whether the node is sticky.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'The Unix timestamp when the node was created.',
  KEY `term_node` (`tid`,`sticky`,`created`),
  KEY `nid` (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Maintains denormalized information about node/term...';

-- Data exporting was unselected.


-- Dumping structure for table apex.taxonomy_term_data
DROP TABLE IF EXISTS `taxonomy_term_data`;
CREATE TABLE IF NOT EXISTS `taxonomy_term_data` (
  `tid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique term ID.',
  `vid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The taxonomy_vocabulary.vid of the vocabulary to which the term is assigned.',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'The term name.',
  `description` longtext COMMENT 'A description of the term.',
  `format` varchar(255) DEFAULT NULL COMMENT 'The filter_format.format of the description.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'The weight of this term in relation to other terms.',
  PRIMARY KEY (`tid`),
  KEY `taxonomy_tree` (`vid`,`weight`,`name`),
  KEY `vid_name` (`vid`,`name`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores term information.';

-- Data exporting was unselected.


-- Dumping structure for table apex.taxonomy_term_hierarchy
DROP TABLE IF EXISTS `taxonomy_term_hierarchy`;
CREATE TABLE IF NOT EXISTS `taxonomy_term_hierarchy` (
  `tid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Primary Key: The taxonomy_term_data.tid of the term.',
  `parent` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Primary Key: The taxonomy_term_data.tid of the term’s parent. 0 indicates no parent.',
  PRIMARY KEY (`tid`,`parent`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores the hierarchical relationship between terms.';

-- Data exporting was unselected.


-- Dumping structure for table apex.taxonomy_vocabulary
DROP TABLE IF EXISTS `taxonomy_vocabulary`;
CREATE TABLE IF NOT EXISTS `taxonomy_vocabulary` (
  `vid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique vocabulary ID.',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'Name of the vocabulary.',
  `machine_name` varchar(255) NOT NULL DEFAULT '' COMMENT 'The vocabulary machine name.',
  `description` longtext COMMENT 'Description of the vocabulary.',
  `hierarchy` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'The type of hierarchy allowed within the vocabulary. (0 = disabled, 1 = single, 2 = multiple)',
  `module` varchar(255) NOT NULL DEFAULT '' COMMENT 'The module which created the vocabulary.',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT 'The weight of this vocabulary in relation to other vocabularies.',
  PRIMARY KEY (`vid`),
  UNIQUE KEY `machine_name` (`machine_name`),
  KEY `list` (`weight`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores vocabulary information.';

-- Data exporting was unselected.


-- Dumping structure for table apex.url_alias
DROP TABLE IF EXISTS `url_alias`;
CREATE TABLE IF NOT EXISTS `url_alias` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'A unique path alias identifier.',
  `source` varchar(255) NOT NULL DEFAULT '' COMMENT 'The Drupal path this alias is for; e.g. node/12.',
  `alias` varchar(255) NOT NULL DEFAULT '' COMMENT 'The alias for this path; e.g. title-of-the-story.',
  `language` varchar(12) NOT NULL DEFAULT '' COMMENT 'The language this alias is for; if ’und’, the alias will be used for unknown languages. Each Drupal path can have an alias for each supported language.',
  PRIMARY KEY (`pid`),
  KEY `alias_language_pid` (`alias`,`language`,`pid`),
  KEY `source_language_pid` (`source`,`language`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='A list of URL aliases for Drupal paths; a user may visit...';

-- Data exporting was unselected.


-- Dumping structure for table apex.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Primary Key: Unique user ID.',
  `name` varchar(60) NOT NULL DEFAULT '' COMMENT 'Unique user name.',
  `pass` varchar(128) NOT NULL DEFAULT '' COMMENT 'User’s password (hashed).',
  `mail` varchar(254) DEFAULT '' COMMENT 'User’s e-mail address.',
  `theme` varchar(255) NOT NULL DEFAULT '' COMMENT 'User’s default theme.',
  `signature` varchar(255) NOT NULL DEFAULT '' COMMENT 'User’s signature.',
  `signature_format` varchar(255) DEFAULT NULL COMMENT 'The filter_format.format of the signature.',
  `created` int(11) NOT NULL DEFAULT '0' COMMENT 'Timestamp for when user was created.',
  `access` int(11) NOT NULL DEFAULT '0' COMMENT 'Timestamp for previous time user accessed the site.',
  `login` int(11) NOT NULL DEFAULT '0' COMMENT 'Timestamp for user’s last login.',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'Whether the user is active(1) or blocked(0).',
  `timezone` varchar(32) DEFAULT NULL COMMENT 'User’s time zone.',
  `language` varchar(12) NOT NULL DEFAULT '' COMMENT 'User’s default language.',
  `picture` int(11) NOT NULL DEFAULT '0' COMMENT 'Foreign key: file_managed.fid of user’s picture.',
  `init` varchar(254) DEFAULT '' COMMENT 'E-mail address used for initial account creation.',
  `data` longblob COMMENT 'A serialized array of name value pairs that are related to the user. Any form values posted during user edit are stored and are loaded into the $user object during user_load(). Use of this field is discouraged and it will likely disappear in a future...',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `name` (`name`),
  KEY `access` (`access`),
  KEY `created` (`created`),
  KEY `mail` (`mail`),
  KEY `picture` (`picture`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores user data.';

-- Data exporting was unselected.


-- Dumping structure for table apex.users_roles
DROP TABLE IF EXISTS `users_roles`;
CREATE TABLE IF NOT EXISTS `users_roles` (
  `uid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Primary Key: users.uid for user.',
  `rid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Primary Key: role.rid for role.',
  PRIMARY KEY (`uid`,`rid`),
  KEY `rid` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Maps users to roles.';

-- Data exporting was unselected.


-- Dumping structure for table apex.variable
DROP TABLE IF EXISTS `variable`;
CREATE TABLE IF NOT EXISTS `variable` (
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT 'The name of the variable.',
  `value` longblob NOT NULL COMMENT 'The value of the variable.',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Named variable/value pairs created by Drupal core or any...';

-- Data exporting was unselected.


-- Dumping structure for table apex.watchdog
DROP TABLE IF EXISTS `watchdog`;
CREATE TABLE IF NOT EXISTS `watchdog` (
  `wid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique watchdog event ID.',
  `uid` int(11) NOT NULL DEFAULT '0' COMMENT 'The users.uid of the user who triggered the event.',
  `type` varchar(64) NOT NULL DEFAULT '' COMMENT 'Type of log message, for example "user" or "page not found."',
  `message` longtext NOT NULL COMMENT 'Text of log message to be passed into the t() function.',
  `variables` longblob NOT NULL COMMENT 'Serialized array of variables that match the message string and that is passed into the t() function.',
  `severity` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'The severity level of the event; ranges from 0 (Emergency) to 7 (Debug)',
  `link` varchar(255) DEFAULT '' COMMENT 'Link to view the result of the event.',
  `location` text NOT NULL COMMENT 'URL of the origin of the event.',
  `referer` text COMMENT 'URL of referring page.',
  `hostname` varchar(128) NOT NULL DEFAULT '' COMMENT 'Hostname of the user who triggered the event.',
  `timestamp` int(11) NOT NULL DEFAULT '0' COMMENT 'Unix timestamp of when event occurred.',
  PRIMARY KEY (`wid`),
  KEY `type` (`type`),
  KEY `uid` (`uid`),
  KEY `severity` (`severity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Table that contains logs of all system events.';

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
