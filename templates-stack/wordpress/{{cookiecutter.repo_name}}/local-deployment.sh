#!/bin/bash

source .env
wp_config_path=$WP_CONFIG_PATH


# Check if the wp-config file exists
if [ -f "$wp_config_path" ]; then
    # Update database connection details
    LC_CTYPE=C LANG=C sed -i -e "s/define( 'DB_NAME', '.*' );/define( 'DB_NAME', '$STAGING_DB_NAME' );/" $wp_config_path
    LC_CTYPE=C LANG=C sed -i -e "s/define( 'DB_USER', '.*' );/define( 'DB_USER', '$STAGING_DB_USER' );/" $wp_config_path
    LC_CTYPE=C LANG=C sed -i -e "s/define( 'DB_PASSWORD', '.*' );/define( 'DB_PASSWORD', '$STAGING_DB_PASSWORD' );/" $wp_config_path
    LC_CTYPE=C LANG=C sed -i -e "s/define( 'DB_HOST', '.*' );/define( 'DB_HOST', '$WP_HOST_DB_NAME:$WP_HOST_DB_PORT' );/" $wp_config_path
else
    echo "WordPress configuration file not found: $wp_config_path"
fi

# Adjust local database init script
LC_CTYPE=C LANG=C sed -i -e "s/fe45224d/$PROD_DB_NAME/" local-init.sql
LC_CTYPE=C LANG=C sed -i -e "s/dk583/$WP_DB_PREFIX/" local-init.sql
LC_CTYPE=C LANG=C sed -i -e "s#https://www.example.com#$PROD_WP_BASE_URL#" local-init.sql
