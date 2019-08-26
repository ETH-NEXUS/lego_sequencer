import json
import re
from time import sleep, time

import requests

from sequencer.cache import cache

# above disclaimer copied from NCBI's web_blast.pl reference file.
# code adapted to python3 by faisal alq.
# ===========================================================================
#
#                            PUBLIC DOMAIN NOTICE
#               National Center for Biotechnology Information
#
# This software/database is a "United States Government Work" under the
# terms of the United States Copyright Act.  It was written as part of
# the author's official duties as a United States Government employee and
# thus cannot be copyrighted.  This software/database is freely available
# to the public for use. The National Library of Medicine and the U.S.
# Government have not placed any restriction on its use or reproduction.
#
# Although all reasonable efforts have been taken to ensure the accuracy
# and reliability of the software and data, the NLM and the U.S.
# Government do not and cannot warrant the performance or results that
# may be obtained by using this software or data. The NLM and the U.S.
# Government disclaim all warranties, express or implied, including
# warranties of performance, merchantability or fitness for any particular
# purpose.
#
# Please cite the author in any work or product based on this material.
#
# ===========================================================================
#
# This code is for example purposes only.
#
# Please refer to https://ncbi.github.io/blast-cloud/dev/api.html
# for a complete list of allowed parameters.
#
# Please do not submit or retrieve more than one request every two seconds.
#
# Results will be kept at NCBI for 24 hours. For best batch performance,
# we recommend that you submit requests after 2000 EST (0100 GMT) and
# retrieve results before 0500 EST (1000 GMT).
#
# ===========================================================================
#
# return codes:
#     0 - success
#     1 - invalid arguments
#     2 - no hits found
#     3 - rid expired
#     4 - search failed
#     5 - unknown error
#
# ===========================================================================

from ..default_settings import MOCK_BLAST
BLAST_URL = (
    "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"
    if not MOCK_BLAST else "http://localhost:5000/api/mock_blast"
)


def blast_sequence(sequence, database, program='blastn', timeout=None):
    """
    Initiate a BLAST request against NCBI's servers, wait for result, then eventually return it.

    :param sequence: the query sequence, a string of (A,C,T,G)s
    :param database: a string identifying the database against which to run the query
    :param program: the program to use to execute the query, one of (megablast, blastn, blastp, rpsblast, blastx,
    tblastn, tblastx)
    :param timeout: time to wait in seconds (past the estimate) for a result before aborting, None will wait forever
    :return: incremental status updates of the form {'status': <text>}, eventually ending in {'results': [...]}
    """

    # # pre-step: check if we have it cached
    cache_key = 'BLAST:%s_%s_%s' % (sequence, database, program)
    cached_val = cache.get(cache_key)
    if cached_val:
        yield {'status': "Sequence found in cache, returning it."}
        yield {'results': cached_val}
        return

    # ------------------------------------------------------
    # --- step 1. send initial request
    # ------------------------------------------------------

    resp = requests.post(BLAST_URL, data={
        'CMD': 'Put',
        'PROGRAM': program,
        'DATABASE': database,
        'QUERY': sequence
    })

    # parse out result id, estimated time to completion
    result_id_match = re.search(r'^ {4}RID = (.*$)', resp.text, flags=re.MULTILINE)
    estimated_completion_match = re.search(r'^ {4}RTOE = (.*$)', resp.text, flags=re.MULTILINE)

    try:
        result_id = result_id_match.group(1)
        estimated_completion_secs = int(estimated_completion_match.group(1))
    except AttributeError:
        raise Exception("Unable to parse request id or completion time out of response")

    # ------------------------------------------------------
    # --- step 2. wait estimated time until we should check for response
    # ------------------------------------------------------

    yield {'status': "Waiting %d seconds for results for %s to be ready..." % (estimated_completion_secs, result_id)}
    sleep(estimated_completion_secs)
    yield {'status': "...done waiting, checking now."}

    # ------------------------------------------------------
    # --- step 3. poll regularly for completion
    # ------------------------------------------------------

    # establish timeout if it was specified
    end_time = time() + timeout if timeout else None

    while True:
        if end_time and time() > end_time:
            raise Exception("Timeout of %d seconds exceeded while waiting for results" % timeout)

        # poll for results using the result ID
        resp = requests.get(BLAST_URL, params={
            "CMD": "Get",
            "FORMAT_OBJECT": "SearchInfo",
            "RID": result_id
        })

        # parse out the status
        status_match = re.search(r'\s+Status=([A-Z]+)', resp.text, flags=re.MULTILINE)

        if not status_match:
            raise Exception("No parseable status in response")

        status = status_match.group(1)

        if status == 'WAITING':
            yield {'status': "Not ready, trying again in 5 seconds..."}
            sleep(5)
            continue
        elif status == 'UNKNOWN':
            raise Exception("Search for %s expired, terminating" % result_id)
        elif status == 'READY':
            yield {'status': "Completed! Fetching results..."}
            break
        else:
            yield {'status': "No hits found"}
            return None

    # ------------------------------------------------------
    # --- step 4. retrieve results
    # ------------------------------------------------------

    # we're done waiting, fetch results and return them
    resp = requests.get(BLAST_URL, params={
        "CMD": "Get",
        "FORMAT_TYPE": "JSON2_S",
        "RID": result_id
    })

    # populate the cache with the results and return the result
    parsed_result = json.loads(resp.text)
    cache.set(cache_key, parsed_result)
    # BLAST_CACHE[cache_key] = parsed_result

    yield {'results': parsed_result}
