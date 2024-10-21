<!-- BEGIN_ANSIBLE_DOCS -->

# Ansible Role: trippsc2.mssql.install
Version: 1.3.0

This role installs Microsoft SQL Server.

## Requirements

| Platform | Versions |
| -------- | -------- |
| EL | <ul><li>8</li><li>9</li></ul> |
| Ubuntu | <ul><li>focal</li><li>jammy</li></ul> |
| Windows | <ul><li>2019</li><li>2022</li></ul> |

## Dependencies

| Collection |
| ---------- |
| ansible.posix |
| ansible.windows |
| chocolatey.chocolatey |
| community.general |
| community.hashi_vault |
| community.windows |
| trippsc2.hashi_vault |
| trippsc2.windows |

## Role Arguments
|Option|Description|Type|Required|Choices|Default|
|---|---|---|---|---|---|
| mssql_host | <p>The hostname used to connect to the SQL Server instance for configuration.</p> | str | no |  | {{ ansible_host }} |
| mssql_port | <p>The port used to connect to the SQL Server instance for configuration.</p> | int | no |  | {{ mssql_database_port }} |
| mssql_user | <p>The username used to connect to the SQL Server instance for configuration.</p> | str | no |  | sa |
| mssql_password | <p>The password used to connect to the SQL Server instance for configuration.</p><p>If not defined, the value of *mssql_sa_password* will be used.</p> | str | no |  |  |
| vault_url | <p>The URL for accessing HashiCorp Vault.</p><p>Alternatively, this can be configured through ansible.cfg or environment variables.</p> | str | no |  |  |
| vault_token | <p>The token for accessing HashiCorp Vault.</p><p>Alternatively, this (or any other authentication method) can be configured through ansible.cfg or environment variables.</p> | str | no |  |  |
| mssql_configure_firewall | <p>Whether to configure the host firewall for the SQL Server instance.</p> | bool | no |  | true |
| mssql_configure_monitoring | <p>Whether to configure monitoring for the SQL Server instance.</p> | bool | no |  | false |
| mssql_vault_manage_sa_password | <p>Whether to manage the `sa` password in HashiCorp Vault.</p><p>On Windows, if this is set to `true`, the *mssql_security_mode* must be `mixed`.</p> | bool | no |  | true |
| mssql_vault_manage_monitoring_credentials | <p>Whether to manage the monitoring password in HashiCorp Vault.</p><p>If *mssql_configure_monitoring* is `false`, this is ignored.</p><p>On Windows, if this is set to `true`, the *mssql_security_mode* must be `mixed`.</p> | bool | no |  | false |
| mssql_vault_configure_database_connection | <p>Whether to configure the database connection in HashiCorp Vault.</p><p>On Windows, if this is set to `true`, the *mssql_security_mode* must be `mixed`.</p> | bool | no |  | false |
| mssql_vault_create_secret_engines | <p>Whether to create the secret engines in HashiCorp Vault.</p> | bool | no |  | true |
| mssql_install_database_engine | <p>Whether to install the `SQL Server Database Engine` feature.</p><p>On Linux, this is ignored as it is required for any SQL Server component.</p> | bool | no |  | true |
| mssql_install_agent | <p>Whether to install the `SQL Server Agent` feature.</p><p>On Windows, this is ignored as it is included with the `SQL Server Database Engine` feature automatically.</p><p>On Linux, this will enable SQL Server Agent in the configuration.</p><p>For SQL Server on Linux 2017, this will also install the separate `mssql-server-agent` package.</p> | bool | no |  | true |
| mssql_install_full_text | <p>Whether to install the `Full-Text and Semantic Extractions for Search` feature.</p><p>If *mssql_install_database_engine* is `false`, this must be set to `false`.</p> | bool | no |  | false |
| mssql_install_replication | <p>Whether to install the `Replication` feature.</p><p>If *mssql_install_database_engine* is `false`, this must be set to `false`.</p><p>On Linux, this is ignored as it is included with the `SQL Server Database Engine` feature automatically.</p> | bool | no |  | false |
| mssql_install_analysis_services | <p>Whether to install the `Analysis Services` feature.</p><p>On Linux, this is ignored as this feature is not available.</p> | bool | no |  | false |
| mssql_install_integration_services | <p>Whether to install the `Integration Services` feature.</p> | bool | no |  | false |
| mssql_install_sql_server_management_studio | <p>Whether to install SQL Server Management Studio.</p><p>On Linux, this is ignored as this feature is not available.</p> | bool | no |  | true |
| mssql_sa_password | <p>The password for the `sa` account.</p><p>If *mssql_vault_manage_sa_password* is `true`, this is password will be used if the secret does not exist and will be stored in Vault.  Otherwise, the previously stored password will be used.</p><p>If *mssql_vault_manage_sa_password* is `false`, this is required.</p><p>On Windows, if *mssql_security_mode* is `windows`, this is ignored.</p> | str | no |  |  |
| mssql_vault_sa_mount_point | <p>The mount point for the KV2 secrets engine in HashiCorp Vault.</p><p>If *mssql_vault_manage_sa_password* is `true` (and *mssql_security_mode* is `mixed` on Windows), this is required. Otherwise, it is ignored.</p> | str | no |  |  |
| mssql_vault_sa_secret_path | <p>The path to the secret in HashiCorp Vault.</p><p>If *mssql_vault_manage_sa_password* is `true` (and *mssql_security_mode* is `mixed` on Windows), this is required. Otherwise, it is ignored.</p> | str | no |  |  |
| mssql_version | <p>The version of the SQL Server to install.</p><p>On Linux, this will be validated against the distribution release for compatibility.</p><p>On Windows, this must match the version of the installation media.  This will not be validated.</p> | str | yes | <ul><li>2016</li><li>2017</li><li>2019</li><li>2022</li></ul> |  |
| mssql_firewall_type | <p>The type of firewall to configure on Linux systems.</p><p>On Windows, this is ignored.</p><p>On EL systems, this defaults to `firewalld`.</p><p>On Ubuntu systems, this defaults to `ufw`.</p> | str | no | <ul><li>firewalld</li><li>ufw</li></ul> |  |
| mssql_database_port | <p>The port for the SQL Server instance.</p><p>On Windows, this is ignored.</p> | int | no |  | 1433 |
| mssql_product_key | <p>The product key to use for the SQL Server installation.</p><p>On Linux, if *mssql_edition* is not defined, this is required.</p><p>On Windows, if the installation media is not pre-activated, this is required.</p> | str | no |  |  |
| mssql_database_edition | <p>The edition of the SQL Server to install.</p><p>On Linux, if *mssql_product_key* is not defined, this is required.  Otherwise, this is ignored.</p><p>On Windows, this is ignored and the edition is determined by the installation media.</p> | str | no | <ul><li>evaluation</li><li>developer</li><li>express</li><li>web</li><li>standard</li><li>enterprise</li><li>enterprise_core</li></ul> |  |
| mssql_integration_edition | <p>The edition of the SQL Server to install for SSIS.</p><p>If *mssql_install_integration_services* is `false`, this is ignored.</p><p>On Linux, if *mssql_install_integration_services* is `true` and *mssql_product_key* is not defined, this is required.  Otherwise, this is ignored.</p><p>On Windows, this is ignored and the edition is determined by the installation media.</p> | str | no | <ul><li>evaluation</li><li>developer</li><li>express</li><li>web</li><li>standard</li><li>enterprise</li></ul> |  |
| mssql_database_lcid | <p>The locale ID to use for the SQL Server setup process.</p><p>On Windows, this is ignored.</p><p>Reference: https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-fulltext-languages-transact-sql?view=sql-server-ver16</p> | int | no |  | 1033 |
| mssql_use_english_setup_locale | <p>Whether to use the English locale for the SQL Server setup process.</p><p>On Linux, this is ignored.</p> | bool | no |  | true |
| mssql_database_default_collation | <p>The default collation for the SQL Server instance.</p> | str | no |  | SQL_Latin1_General_CP1_CI_AS |
| mssql_as_collation | <p>The collation for the SQL Server Analysis Services instance.</p><p>If *mssql_install_analysis_services* is `false`, this is ignored.</p> | str | no |  | Latin1_General_CI_AS |
| mssql_database_backup_path | <p>The path to the SQL Server backup directory.</p><p>On Linux, this defaults to `/var/opt/mssql/data`.</p><p>On Windows, this defaults to `<*mssql_instance_path*>\MSSQL<MSSQL-version>.<*mssql_instance_id*>\MSSQL\Backup`.</p> | path | no |  |  |
| mssql_database_data_path | <p>The path to the SQL Server DB data directory.</p><p>On Windows, this is ignored.</p> | path | no |  | /var/opt/mssql/data |
| mssql_database_log_path | <p>The path to the SQL Server DB log directory.</p><p>On Windows, this is ignored.</p> | path | no |  | /var/opt/mssql/data |
| mssql_database_dump_path | <p>The path to the SQL Server dump directory.</p><p>On Windows, this is ignored.</p> | path | no |  | /var/opt/mssql/log |
| mssql_database_master_data_file_path | <p>The path to the SQL Server master data file.</p><p>On Windows, this is ignored.</p> | path | no |  | /var/opt/mssql/data/master.mdf |
| mssql_database_master_log_file_path | <p>The path to the SQL Server master log file.</p><p>On Windows, this is ignored.</p> | path | no |  | /var/opt/mssql/data/mastlog.ldf |
| mssql_database_error_log_file_path | <p>The path to the SQL Server error log file.</p><p>On Windows, this is ignored.</p> | path | no |  |  |
| mssql_database_memory_limit_in_mb | <p>The memory limit for the SQL Server instance.</p><p>This defaults to 80% of the total system memory.</p><p>On Windows, this is ignored.</p> | int | no |  |  |
| mssql_database_customer_feedback_enabled | <p>Whether to enable customer feedback for the SQL Server instance.</p><p>On Windows, this is ignored.</p> | bool | no |  | false |
| mssql_database_tls_force_encryption | <p>Whether to force encryption for the SQL Server instance.</p><p>On Windows, this is ignored.</p> | bool | no |  | false |
| mssql_database_tls_certificate_path | <p>The path to the TLS certificate for the SQL Server instance.</p><p>On Windows, this is ignored.</p> | path | no |  |  |
| mssql_database_tls_private_key_path | <p>The path to the TLS private key for the SQL Server instance.</p><p>On Windows, this is ignored.</p> | path | no |  |  |
| mssql_database_tls_protocols | <p>The TLS protocols to enable for the SQL Server instance.</p><p>On Windows, this is ignored.</p> | list of 'str' | no | <ul><li>1.0</li><li>1.1</li><li>1.2</li></ul> | ["1.2"] |
| mssql_enable_active_directory_authentication | <p>Whether to enable Active Directory authentication for the SQL Server instance.</p><p>On Windows, this is ignored.</p> | bool | no |  | false |
| mssql_security_mode | <p>The security mode for the SQL Server instance.</p><p>On Linux, this is ignored.</p> | str | no | <ul><li>mixed</li><li>windows</li></ul> | mixed |
| mssql_active_directory_user | <p>The Active Directory user account to use for SQL Server authentication.</p><p>On Linux, if *mssql_enable_active_directory_authentication* is `true`, this is required.</p><p>On Windows, this is ignored.</p> | str | no |  |  |
| mssql_active_directory_password | <p>The password for the Active Directory user account.</p><p>On Linux, if *mssql_enable_active_directory_authentication* is `true`, this is required.</p><p>On Windows, this is ignored.</p> | str | no |  |  |
| mssql_active_directory_realm | <p>The Active Directory realm to use for SQL Server authentication.</p><p>On Linux, if *mssql_enable_active_directory_authentication* is `true`, this is required.</p><p>On Windows, this is ignored.</p> | str | no |  |  |
| mssql_active_directory_keytab_path | <p>The path to the Active Directory keytab file.</p><p>On Linux, if *mssql_enable_active_directory_authentication* is `true`, this is required.</p><p>On Windows, this is ignored.</p> | path | no |  | /var/opt/mssql/secrets/mssql.keytab |
| mssql_active_directory_admin_username | <p>The Active Directory admin user used to create the keytab.</p><p>On Linux, if *mssql_enable_active_directory_authentication* is `true`, this is required.</p><p>On Windows, this is ignored.</p> | str | no |  |  |
| mssql_active_directory_admin_password | <p>The password for the Active Directory admin user.</p><p>On Linux, if *mssql_enable_active_directory_authentication* is `true`, this is required.</p><p>On Windows, this is ignored.</p> | str | no |  |  |
| mssql_setup_path | <p>The path to the SQL Server setup executable.</p><p>On Linux, this is ignored.</p><p>On Windows, this is required.</p> | path | no |  |  |
| mssql_setup_access_username | <p>The username used to access the SQL Server setup executable, if required.</p><p>On Linux, this is ignored.</p> | str | no |  |  |
| mssql_setup_access_password | <p>The password used to access the SQL Server setup executable, if required.</p><p>On Linux, this is ignored.</p> | str | no |  |  |
| mssql_instance_name | <p>The friendly name of the SQL Server instance to install.</p><p>On Linux, this is ignored.</p> | str | no |  | MSSQLSERVER |
| mssql_instance_id | <p>The ID of the SQL Server instance to install.</p><p>This defaults to the uppercase value of *mssql_instance_name*.</p><p>On Linux, this is ignored.</p> | str | no |  |  |
| mssql_update_enabled | <p>Whether the SQL Server software should be updated during the installation process.</p><p>On Linux, this is ignored.</p> | bool | no |  | true |
| mssql_update_from_microsoft_update | <p>Whether to update the SQL Server software from Microsoft Update.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_update_enabled* is `false`, this is ignored.</p> | bool | no |  | true |
| mssql_update_source | <p>The source of the SQL Server software updates.</p><p>This should be a UNC path or URI to the location of the updates.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_update_enabled* is `false` or *mssql_update_from_microsoft_update* is `true`, this is ignored.</p> | str | no |  | MU |
| mssql_sqm_reporting | <p>Whether to enable SQL Server Customer Experience Improvement Program (CEIP) reporting.</p><p>On Linux, this is ignored.</p> | bool | no |  | false |
| mssql_error_reporting | <p>Whether to enable SQL Server error reporting.</p><p>On Linux, this is ignored.</p> | bool | no |  | false |
| mssql_install_shared_path | <p>The path where the SQL Server shared components will be installed.</p><p>On Linux, this is ignored.</p> | str | no |  | C:\Program Files\Microsoft SQL Server |
| mssql_install_shared_wow64_path | <p>The path where the SQL Server shared components will be installed on 64-bit systems.</p><p>On Linux, this is ignored.</p> | str | no |  | C:\Program Files (x86)\Microsoft SQL Server |
| mssql_instance_path | <p>The path where the SQL Server instance will be installed.</p><p>On Linux, this is ignored.</p> | str | no |  | {{ mssql_install_shared_path }} |
| mssql_named_pipes_enabled | <p>Whether to enable named pipes for the SQL Server instance.</p><p>On Linux, this is ignored.</p> | bool | no |  | false |
| mssql_tcp_enabled | <p>Whether to enable TCP/IP for the SQL Server instance.</p><p>On Linux, this is ignored.</p> | bool | no |  | true |
| mssql_setup_process_timeout_in_seconds | <p>The number of seconds to wait for the SQL Server setup process to complete.</p><p>On Linux, this is ignored.</p> | int | no |  | 7200 |
| mssql_sql_server_service_username | <p>The username for the SQL Server service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_service_password | <p>The password for the SQL Server service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_service_startup_type | <p>The startup type for the SQL Server service.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | str | no | <ul><li>Automatic</li><li>Manual</li><li>Disabled</li></ul> |  |
| mssql_sql_server_agent_service_username | <p>The username for the SQL Server Agent service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_agent_service_password | <p>The password for the SQL Server Agent service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_agent_service_startup_type | <p>The startup type for the SQL Server Agent service.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | str | no | <ul><li>Automatic</li><li>Manual</li><li>Disabled</li></ul> |  |
| mssql_database_sysadmin_accounts | <p>The list of accounts to add to the SQL Server sysadmin role.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `true`, this is required.  Otherwise, this is ignored.</p> | list of 'str' | no |  |  |
| mssql_database_user_db_path | <p>The path to the SQL Server data directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | path | no |  | {{ mssql_instance_path }}\MSSQL<version-string>.{{ mssql_instance_id }}\MSSQL\Data |
| mssql_database_user_db_log_path | <p>The path to the SQL Server user database log directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | path | no |  | {{ mssql_database_user_db_path }} |
| mssql_database_temp_db_path | <p>The path to the SQL Server tempdb directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | path | no |  | {{ mssql_database_user_db_path }} |
| mssql_database_temp_db_log_path | <p>The path to the SQL Server tempdb log directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_database_engine* is `false`, this is ignored.</p> | path | no |  | {{ mssql_database_user_db_path }} |
| mssql_full_text_filter_daemon_host_username | <p>The username for the SQL Server Full-Text Filter Daemon Launcher service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_full_text* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_full_text_filter_daemon_host_password | <p>The password for the SQL Server Full-Text Filter Daemon Launcher service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_full_text* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_analysis_services_username | <p>The username for the SQL Server Analysis Services service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_analysis_services_password | <p>The password for the SQL Server Analysis Services service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_analysis_services_startup_type | <p>The startup type of SQL Server Analysis Services instance.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | str | no | <ul><li>Automatic</li><li>Manual</li><li>Disabled</li></ul> |  |
| mssql_as_sysadmin_accounts | <p>The list of accounts to add to the SQL Server Analysis Services sysadmin role.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `true`, this is required.  Otherwise, this is ignored.</p> | list of 'str' | no |  |  |
| mssql_as_data_path | <p>The path to the SQL Server Analysis Services data directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | path | no |  | {{ mssql_instance_path }}\MSAS<version-string>.{{ mssql_instance_id }}\OLAP\Data |
| mssql_as_log_path | <p>The path to the SQL Server Analysis Services log directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | path | no |  | {{ mssql_instance_path }}\MSAS<version-string>.{{ mssql_instance_id }}\OLAP\Log |
| mssql_as_backup_path | <p>The path to the SQL Server Analysis Services backup directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | path | no |  | {{ mssql_instance_path }}\MSAS<version-string>.{{ mssql_instance_id }}\OLAP\Backup |
| mssql_as_temp_path | <p>The path to the SQL Server Analysis Services temp directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | path | no |  | {{ mssql_instance_path }}\MSAS<version-string>.{{ mssql_instance_id }}\OLAP\Temp |
| mssql_as_config_path | <p>The path to the SQL Server Analysis Services config directory.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | path | no |  | {{ mssql_instance_path }}\MSAS<version-string>.{{ mssql_instance_id }}\OLAP\Config |
| mssql_as_server_mode | <p>The server mode for the SQL Server Analysis Services instance.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | str | no | <ul><li>multidimensional</li><li>tabular</li><li>powerpivot</li></ul> | Tabular |
| mssql_as_tempdb_file_count | <p>The number of tempdb files for the SQL Server Analysis Services instance.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | int | no |  | 8 |
| mssql_as_tempdb_file_growth | <p>The size of the tempdb files for the SQL Server Analysis Services instance.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | int | no |  | 64 |
| mssql_as_tempdb_log_file_size | <p>The size of the tempdb log file for the SQL Server Analysis Services instance.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | int | no |  | 8 |
| mssql_as_tempdb_log_file_growth | <p>The growth of the tempdb log file for the SQL Server Analysis Services instance.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_analysis_services* is `false`, this is ignored.</p> | int | no |  | 64 |
| mssql_sql_server_integration_services_username | <p>The username for the SQL Server Integration Services service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_integration_services* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_integration_services_password | <p>The password for the SQL Server Integration Services service account.</p><p>If not defined, the default service account will be used.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_integration_services* is `false`, this is ignored.</p> | str | no |  |  |
| mssql_sql_server_integration_services_startup_type | <p>The startup type of SQL Server Integration Services instance.</p><p>On Linux, this is ignored.</p><p>On Windows, if *mssql_install_integration_services* is `false`, this is ignored.</p> | str | no | <ul><li>Automatic</li><li>Manual</li><li>Disabled</li></ul> |  |
| mssql_failover_cluster_group_name | <p>The name of the failover cluster group.</p><p>On Linux, this is ignored.</p> | str | no |  |  |
| mssql_failover_cluster_ip_address | <p>The IP address of the failover cluster.</p><p>On Linux, this is ignored.</p> | str | no |  |  |
| mssql_failover_cluster_network_name | <p>The name of the failover cluster network.</p><p>On Linux, this is ignored.</p> | str | no |  |  |
| mssql_skip_reboot | <p>Whether to skip the reboot after the SQL Server installation.</p><p>On Linux, this is ignored.</p> | bool | no |  | true |
| mssql_monitoring_user | <p>The monitoring user account to use for SQL Server monitoring.</p><p>If *mssql_configure_monitoring* is `true`, this is required. Otherwise, this is ignored.</p> | str | no |  |  |
| mssql_monitoring_password | <p>The password for the monitoring user account.</p><p>If *mssql_configure_monitoring* is `false`, this is ignored.</p><p>If *mssql_vault_manage_monitoring_credentials* is `true` and this is defined, the password will be looked in HashiCorp Vault and this value will be stored there if the secret does not exist.</p><p>If *mssql_vault_manage_monitoring_credentials* is `true` and this is not defined, the password will be looked up from HashiCorp Vault and a value will be generate if the secret does not exist.</p><p>If *mssql_vault_manage_monitoring_credentials* is `false`, this is required.</p> | str | no |  |  |
| mssql_vault_monitoring_mount_point | <p>The mount point at which the monitoring password secret will be stored in HashiCorp Vault.</p><p>If *mssql_vault_manage_monitoring_credentials* is `true`, this is required.  Otherwise, this is ignored.</p> | str | no |  |  |
| mssql_vault_monitoring_secret_path | <p>The path within the mount point at which the monitoring password secret will be stored in HashiCorp Vault.</p><p>If *mssql_vault_manage_monitoring_credentials* is `true`, this is required.  Otherwise, this is ignored.</p> | str | no |  |  |
| mssql_vault_database_mount_point | <p>The mount point of the database secret engine in HashiCorp Vault.</p><p>If *mssql_vault_configure_database_connection* is `true`, this is required.  Otherwise, this is ignored.</p> | str | no |  |  |
| mssql_vault_database_connection_name | <p>The name of the database connection in HashiCorp Vault.</p><p>If *mssql_vault_configure_database_connection* is `true`, this is required.  Otherwise, this is ignored.</p> | str | no |  | {{ inventory_hostname }} |
| mssql_vault_database_connection_username | <p>The username for the database connection in HashiCorp Vault.</p><p>If *mssql_vault_configure_database_connection* is `true`, this is required.  Otherwise, this is ignored.</p> | str | no |  | vault |
| mssql_vault_database_connection_temporary_password | <p>The temporary password for the database connection in HashiCorp Vault.  This password is only used until the connection is created in HashiCorp Vault, at which time it will be rotated.</p><p>If *mssql_vault_configure_database_connection* is `true`, this is required.  Otherwise, this is ignored.</p> | str | no |  | TemporaryPassword123! |
| mssql_vault_database_connection_hostname | <p>The hostname used to connect to the HashiCorp Vault instance.</p><p>If *mssql_vault_configure_database_connection* are `true`, this is required. Otherwise, this is ignored.</p> | str | no |  |  |
| mssql_vault_database_connection_port | <p>The port used to connect to the HashiCorp Vault instance.</p><p>If *mssql_vault_configure_database_connection* are `true`, this is required. Otherwise, this is ignored.</p> | int | no |  | {{ mssql_database_port }} |


## License
MIT

## Author and Project Information
Jim Tarpley
<!-- END_ANSIBLE_DOCS -->
