<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the website, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://developer.wordpress.org/advanced-administration/wordpress/wp-config/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'tecnixview' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', 'root' );

/** Database hostname (MariaDB en pod dev-stack, puerto publicado en el host) */
define( 'DB_HOST', '127.0.0.1' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', 'utf8mb4_general_ci' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'MSX__uFDIzy[^Z<,K0y0k)P+/a6J&#*28?@z8]?Bb=M,- QRDfp4B_^m5Asys!s2' );
define( 'SECURE_AUTH_KEY',  '~n]T;rOMSqo!|,Zmn%l&Z?h=zC_*@yqqtJA;v]f${P_RrU7pXa?=k4caw@ui(FoH' );
define( 'LOGGED_IN_KEY',    '-^;ak%BE9z&LD8@ELN7@2E`M<1&*gDo]}]bMsL1bUL82z/n~iqANA%CCepqm{Cvr' );
define( 'NONCE_KEY',        '8CMwO~DjMrzriG_yJV[G:c%uPd8#VPY0C-_]zE`d5g5|PL2GE03<#)O+>GIs`XYZ' );
define( 'AUTH_SALT',        '(8){>+.(0[rUc5,L%>?W^k4P8KUxdHGHqjG%+_[#Z3%>^XRGXKp#$+>n[vrR4!}m' );
define( 'SECURE_AUTH_SALT', '!kPvz{+3_fKDNQ5Hk0W,Pb]KJ^N>2>ov2YPvnO%v:[2GKTP3abwX$pb7q|IVi*4M' );
define( 'LOGGED_IN_SALT',   'yKpz02(Da<l-mg|WOvku,Jty5`cOWf3J4,L1BoZ[N4?XYvLS8_OLb&>;gQ0l5l::' );
define( 'NONCE_SALT',       '05Os*]qlV7dlrLTh]<!4@{h2-FtvFq[58dP$jS5[i{|Qo!:I#; e`+S@c U6Fel,' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 *
 * At the installation time, database tables are created with the specified prefix.
 * Changing this value after WordPress is installed will make your site think
 * it has not been installed.
 *
 * @link https://developer.wordpress.org/advanced-administration/wordpress/wp-config/#table-prefix
 */
$table_prefix = 'tcvw_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */

/** URLs locales (servidor PHP en dev-stack puerto 8080) */
define( 'WP_HOME', 'http://127.0.0.1:8888' );
define( 'WP_SITEURL', 'http://127.0.0.1:8888' );



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
