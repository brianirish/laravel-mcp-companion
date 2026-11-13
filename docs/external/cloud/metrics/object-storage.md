Source: https://laravel.com/cloud/docs/metrics/object-storage.md

# Object storage metrics

Understand the operations, errors, egress, and size metrics for your Laravel Object Storage buckets.

## Introduction

Laravel Cloud shows metrics for each [Laravel Object Storage](https://laravel.com/cloud/docs/resources/object-storage) bucket in two places:

* **The bucket's page:** navigate to **Organization > Resources > Object storage**, click your bucket, and review the **Metrics** section.
* **The environment's Metrics tab:** open **Monitoring > Metrics** in any environment to see a card for each bucket attached to it. These cards also show the bucket's **Size**.

Metrics cover the whole bucket, even when several environments share it. Use the time range selector to choose a period, depending on your plan's [retention period](https://laravel.com/cloud/docs/metrics/overview#time-ranges-and-retention). Each headline value is the total for the selected range.

## Operations

The **Operations** chart counts the requests made to your bucket, grouped by the class used for [pricing](https://laravel.com/cloud/docs/pricing#laravel-object-storage):

* **Class A:** operations that write or list data, such as uploading a file or listing a directory's contents.
* **Class B:** operations that read data, such as downloading a file or checking whether it exists.

Some operations, such as deleting a file, belong to neither class and do not appear in the chart. Class A operations cost more than Class B operations, so investigate a high Class A count. For example, an application that lists a directory on every request adds one Class A operation to every request.

## Errors

The **Errors** chart counts requests to your bucket that returned an error:

* **4XX:** request errors, such as a request for a file that does not exist, or a request with invalid credentials.
* **5XX:** server errors on the storage side.

A steady stream of **4XX** errors often means your application requests files that were moved or deleted, or uses outdated credentials. Occasional **5XX** errors are usually temporary. Retrying the request typically succeeds.

## Egress

The **Egress** chart shows the amount of data your bucket sent in response to requests, such as files your application or your users downloaded. The headline **Total** value is the data sent during the selected range.

## Size

Bucket cards on the environment's **Metrics** tab show the bucket's **Size**, which is the total size of the files stored in it at the end of the selected range.
