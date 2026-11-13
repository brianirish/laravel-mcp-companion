Source: https://herd.laravel.com/docs/macos/technology/php-extensions.md

# PHP Extensions

# Included PHP Extensions

Herd includes the most common PHP extensions that also come pre-installed on any [Laravel Forge](https://forge.laravel.com)  provisioned server. This means that you can use the following extensions without any additional setup:

### bcmath

The BCMath extension provides arbitrary-precision arithmetic. It allows you to work with large numbers and perform mathematical operations with high precision, which is particularly useful in financial applications.

### bz2

The BZ2 extension enables data compression using the bzip2 algorithm. This reduces file sizes and improves storage efficiency.

### calendar

The Calendar extension provides functions to convert between different calendar formats. It supports conversions between Julian, Gregorian, and Jewish calendars, among others.

### ctype

The Ctype extension provides functions to check for and convert between character types. It is useful for validating and sanitizing text input.

### curl

The cURL extension enables HTTP requests using various protocols. It is essential for integrating with third-party APIs and fetching external data.

### dba

The DBA extension allows you to interact with flat-file databases, like DBM. It provides a simple way to store and retrieve key-value pairs.

### dom

The DOM extension provides a complete API for working with XML documents via the Document Object Model. It simplifies XML parsing and manipulation.

### exif

The Exif extension reads Exchangeable Image File (Exif) metadata from images. It allows you to access camera information, orientation, GPS data, and more.

### ffi

The Foreign Function Interface (FFI) extension allows PHP to call functions written in other languages (like C) directly, providing the ability to use libraries written in those languages.

### fileinfo

The Fileinfo extension detects file types based on file signatures. It is useful for security checks and content-type validation.

### filter

The Filter extension provides a simple way to sanitize and validate data, particularly user input, ensuring data integrity and security.

### ftp

The FTP extension provides functions for accessing files on FTP servers. It simplifies the process of transferring files over FTP.

### gd

The GD extension offers functions for creating and manipulating images. It supports several image formats and provides capabilities like resizing, cropping, and drawing shapes.

### gmp

The GMP extension provides functions for arbitrary-precision arithmetic using the GNU Multiple Precision (GMP) library. It is ideal for cryptographic applications.

### iconv

The Iconv extension provides functions for converting between different character encodings. It ensures text compatibility across various languages and encoding formats.

### igbinary

The Igbinary extension provides an alternative binary serialization format. It reduces storage space and speeds up data deserialization.

### imagick

The Imagick extension provides an interface to the ImageMagick library, enabling advanced image processing capabilities, such as resizing, blurring, and color correction.

### imap

The IMAP extension provides functions to interact with email servers using IMAP, POP3, and NNTP protocols. It is useful for reading, composing, and sending emails.

### intl

The Intl extension provides internationalization functions, including formatting numbers, dates, currencies according to locale, and handling text in different languages.

### ldap

The LDAP extension allows PHP to interact with LDAP (Lightweight Directory Access Protocol) directories. It is useful for managing centralized user directories and authenticating users.

### lz4

The LZ4 extension provides fast compression and decompression using the LZ4 algorithm. It is suitable for applications requiring high-speed data compression.

### mbstring

The Multibyte String (Mbstring) extension provides functions to handle multibyte encodings, making it essential for processing non-ASCII text.

### mongodb

The MongoDB extension allows PHP to interact with MongoDB databases. It is essential for building applications that use MongoDB as the data store.

### mysqli

The MySQLi extension provides an improved interface to MySQL databases. It supports prepared statements, transactions, and multiple query results.

### opcache

The Opcache extension improves PHP performance by caching precompiled script bytecode, reducing the need for PHP to recompile scripts on each request.

### openssl

The OpenSSL extension enables secure data transmission using SSL and TLS protocols. It provides functions for encryption, decryption, and handling of digital certificates.

### pcntl

The PCNTL extension enables process control functions, allowing you to manage parallel processing and signal handling in PHP.

### pdo

The PHP Data Objects (PDO) extension provides a unified interface for database access. It supports prepared statements and various database drivers.

### pdo\_mysql

The PDO\_MySQL extension provides a PDO driver for MySQL databases, enabling secure and efficient access to MySQL using prepared statements.

### pdo\_pgsql

The PDO\_PgSQL extension provides a PDO driver for PostgreSQL databases, allowing secure and efficient access to PostgreSQL using prepared statements.

### pdo\_sqlite

The PDO\_SQLite extension provides a PDO driver for SQLite databases, facilitating lightweight and embedded database access with minimal configuration.

### pdo\_sqlsrv

The PDO\_SQLSRV extension provides a PDO driver for Microsoft SQL Server databases, enabling secure and efficient access to SQL Server using prepared statements.

### pgsql

The PgSQL extension provides native PostgreSQL database functions, offering comprehensive access to PostgreSQL features.

### phar

The Phar extension enables packaging PHP applications into a single file archive (PHAR). It simplifies application distribution and deployment.

### posix

The POSIX extension provides functions for POSIX-like system calls, useful for handling process management and file permissions.

### readline

The Readline extension provides interactive command-line editing capabilities. It enhances the CLI experience by supporting history and line editing.

### redis

The Redis extension allows PHP to interact with the Redis in-memory data structure store. It is essential for caching, message brokering, and real-time data processing.

### session

The Session extension manages session data between requests. It simplifies storing and retrieving user-specific data securely.

### shmop

The SHMOP extension allows PHP to read and write shared memory segments. It is useful for IPC (Inter-Process Communication).

### simplexml

The SimpleXML extension provides a simple interface for parsing and manipulating XML documents. It makes working with XML data intuitive and efficient.

### soap

The SOAP extension provides functions for building and consuming SOAP-based web services. It simplifies integrating with legacy systems that use SOAP.

### sockets

The Sockets extension provides functions for low-level socket communication, enabling PHP to create network clients and servers.

### sodium

The Sodium extension provides modern cryptography functions. It is useful for encryption, decryption, password hashing, and digital signatures.

### sqlsrv

The SQLSRV extension allows PHP to interact with Microsoft SQL Server databases. It is essential for building applications that use SQL Server as the data store.

### sqlite3

The SQLite3 extension provides native functions for interacting with SQLite databases, offering efficient and lightweight database access.

### sysvmsg

The SysVMsg extension allows PHP to send and receive System V IPC messages. It is useful for messaging between multiple processes.

### sysvsem

The SysVSem extension provides functions for managing System V semaphores, which are useful for synchronizing multiple processes.

### sysvshm

The SysVShm extension allows PHP to read and write System V shared memory segments. It is useful for sharing data between multiple processes.

### tokenizer

The Tokenizer extension provides functions to parse PHP code into tokens, making it useful for syntax highlighting and static analysis.

### xml

The XML extension provides a basic set of tools for working with XML data, allowing for parsing and validation.

### xmlreader

The XMLReader extension provides a fast, non-caching XML parser, suitable for processing large XML files efficiently.

### xmlwriter

The XMLWriter extension offers functions for creating XML documents via a writer API, providing efficient XML generation.

### xsl

The XSL extension allows you to transform XML documents using XSLT stylesheets. It enables flexible data transformation between XML formats.

### zip

The Zip extension provides functions for creating, modifying, and extracting files from ZIP archives, simplifying archive management.

### zlib

The Zlib extension provides functions for data compression and decompression using the zlib library. It is useful for reducing storage space and network bandwidth.

# Installing PHP extensions

You may add additional PHP extensions that are not included out of the box with Herd, by installing them via [Homebrew](https://brew.sh) and [pecl](https://pecl.php.net/). The reason for this is that most of these extension have dependencies and can not be statically compiled, and therefore shipped, with Herd.

## Adding extensions

To install additional extensions via Homebrew, you can compile them with the following commands. At first, Homebrew needs a base PHP for compiling the extension. This base PHP is only used for compiling the extension and Herd keeps using the static binaries, so you can still use the built-in Herd updater for PHP.

```bash theme={null}
brew install php
```

Once PHP is installed via Homebrew, you may install the extension:

```bash theme={null}
pecl install [extension-name]
```

This creates an `[extension].so` extension file that you can now activate and use with Laravel Herd.

The extension can be found at `/opt/homebrew/lib/php/pecl`.

## Activating extensions

You may activate your custom extensions by editing your `php.ini` file.
This file is located at `~/Library/Application Support/Herd/config/php/<version>/php.ini.`.

```bash theme={null}
# Absolute path to the extension.so file
extension=/opt/homebrew/lib/php/pecl/20220829/[extension].so
```
