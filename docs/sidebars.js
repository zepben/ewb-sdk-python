/*
 * Copyright 2021 Zeppelin Bend Pty Ltd
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

module.exports = {
    someSidebar: [
        "sdk-overview",
        {
            type: "category",
            items: ["venv-setup", "intellij-setup"],
            label: "Setup Guide"
        },
        "sdk-data-model",
        "sdk-services",
        "sdk-phases",
        "sdk-tracing",
        "sdk-persistence",
        "sdk-consumer",
        "sdk-protection",
        "sdk-ewb-file-paths",
        {
            type: "category",
            label: "Network State",
            items: ["query-network-state-client", "query-network-state-service", "update-network-state-client", "update-network-state-service"]
        },
    ]
};
